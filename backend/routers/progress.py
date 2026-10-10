"""学习进度：完成课程、进度总览、个性化推荐。"""
import datetime
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .. import database, security
from ..deps import get_current_user
from .achievements import check_achievements

router = APIRouter(prefix="/api", tags=["progress"])

LEVEL_ORDER = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4}
LANG_NAMES = {"en": "英语", "ja": "日语", "ko": "韩语"}


class CompleteBody(BaseModel):
    score: int = Field(ge=0, le=100)


def _stars_for(score: int) -> int:
    if score >= 85:
        return 3
    if score >= 60:
        return 2
    return 1


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(lesson_id: int, body: CompleteBody, user: dict = Depends(get_current_user)):
    lesson = database.fetch_one("SELECT * FROM lessons WHERE id = ?", (lesson_id,))
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")

    today = security.today_iso()
    yesterday = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    existing = database.fetch_one(
        "SELECT * FROM lesson_progress WHERE user_id = ? AND lesson_id = ?", (user["id"], lesson_id)
    )
    is_first_completion = existing is None
    stars = _stars_for(body.score)

    if existing:
        new_score = max(existing["score"], body.score)
        new_stars = max(existing["stars"], stars)
        database.execute(
            "UPDATE lesson_progress SET status='completed', score=?, stars=?, attempts=attempts+1, completed_at=? WHERE id=?",
            (new_score, new_stars, security.now_iso(), existing["id"]),
        )
    else:
        new_score, new_stars = body.score, stars
        database.execute(
            "INSERT INTO lesson_progress (user_id, lesson_id, status, score, stars, attempts, completed_at) VALUES (?,?,?,?,?,?,?)",
            (user["id"], lesson_id, "completed", body.score, stars, 1, security.now_iso()),
        )

    # 更新连续学习天数
    last = user["last_activity_date"]
    if last is None:
        new_streak = 1
    elif last == today:
        new_streak = user["streak"]
    elif last == yesterday:
        new_streak = user["streak"] + 1
    else:
        new_streak = 1

    # 积分（仅首次完成时发放）
    points_gained = new_stars * 10 if is_first_completion else 0

    database.execute(
        "UPDATE users SET streak = ?, last_activity_date = ?, points = points + ? WHERE id = ?",
        (new_streak, today, points_gained, user["id"]),
    )

    conn = database.get_connection()
    newly = check_achievements(conn, user["id"])
    conn.commit()
    conn.close()

    updated = database.fetch_one("SELECT * FROM users WHERE id = ?", (user["id"],))
    return {
        "stars": new_stars,
        "score": new_score,
        "points_gained": points_gained,
        "streak": updated["streak"],
        "points": updated["points"],
        "new_achievements": [
            {"code": a["code"], "name": a["name"], "description": a["description"], "icon": a["icon"]} for a in newly
        ],
    }


@router.get("/progress")
def progress_overview(user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    try:
        courses = conn.execute("SELECT * FROM courses ORDER BY order_index").fetchall()
        course_ids = [c["id"] for c in courses]
        done_rows = {}
        if course_ids:
            q_marks = ",".join("?" for _ in course_ids)
            rows = conn.execute(
                f"SELECT l.course_id, COUNT(*) AS done, AVG(p.score) AS avg_score FROM lesson_progress p JOIN lessons l ON l.id=p.lesson_id WHERE p.user_id = ? AND l.course_id IN ({q_marks}) GROUP BY l.course_id",
                (user["id"], *course_ids),
            ).fetchall()
            done_rows = {r["course_id"]: r for r in rows}

        total_lessons = sum(
            conn.execute("SELECT COUNT(*) AS c FROM lessons WHERE course_id = ?", (c["id"],)).fetchone()["c"]
            for c in courses
        )
        completed_lessons = sum(r["done"] for r in done_rows.values())

        # 按语言统计
        lang_stats = {}
        for code in ["en", "ja", "ko"]:
            lang_courses = [c for c in courses if c["language"] == code]
            total = sum(conn.execute("SELECT COUNT(*) AS c FROM lessons WHERE course_id = ?", (c["id"],)).fetchone()["c"] for c in lang_courses)
            done = sum(done_rows.get(c["id"], {}).get("done", 0) if isinstance(done_rows.get(c["id"]), dict) else 0 for c in lang_courses)
            lang_stats[code] = {"name": LANG_NAMES[code], "total": total, "completed": done}
    finally:
        conn.close()

    today = security.today_iso()
    completed_today = database.fetch_one(
        "SELECT COUNT(*) AS c FROM lesson_progress WHERE user_id = ? AND substr(completed_at,1,10) = ?",
        (user["id"], today),
    )["c"]

    return {
        "stats": {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "completed_today": completed_today,
            "streak": user["streak"],
            "points": user["points"],
            "overall_percent": round(completed_lessons * 100 / total_lessons) if total_lessons else 0,
        },
        "languages": lang_stats,
        "courses": [{"id": c["id"], "title": c["title"], "language": c["language"], "level": c["level"], "icon": c["icon"], "color": c["color"], "done": done_rows.get(c["id"], {}).get("done", 0) if isinstance(done_rows.get(c["id"]), dict) else 0} for c in courses],
    }


@router.get("/recommendations")
def recommendations(user: dict = Depends(get_current_user)):
    targets = json.loads(user["target_languages"] or '["en","ja","ko"]')
    if not targets:
        targets = ["en", "ja", "ko"]

    # 已完成的 lesson_id 集合
    completed = {
        r["lesson_id"]
        for r in database.fetch_all("SELECT lesson_id FROM lesson_progress WHERE user_id = ?", (user["id"],))
    }

    next_items = []
    for code in targets:
        courses = database.fetch_all("SELECT * FROM courses WHERE language = ?", (code,))
        courses.sort(key=lambda c: (LEVEL_ORDER.get(c["level"], 9), c["order_index"]))
        found = None
        for c in courses:
            lessons = database.fetch_all("SELECT * FROM lessons WHERE course_id = ? ORDER BY order_index", (c["id"],))
            for l in lessons:
                if l["id"] not in completed:
                    found = (c, l)
                    break
            if found:
                break
        if found:
            c, l = found
            next_items.append({
                "language": code,
                "language_name": LANG_NAMES[code],
                "course_id": c["id"],
                "course_title": c["title"],
                "course_icon": c["icon"],
                "course_color": c["color"],
                "course_level": c["level"],
                "lesson_id": l["id"],
                "lesson_title": l["title"],
                "lesson_type": l["type"],
            })

    # 建议复习：最近完成且得分较低的课程
    review = database.fetch_all(
        """
        SELECT l.id, l.title, l.type, p.score
        FROM lesson_progress p JOIN lessons l ON l.id = p.lesson_id
        WHERE p.user_id = ? AND p.score < 80
        ORDER BY p.score ASC LIMIT 3
        """,
        (user["id"],),
    )

    return {
        "next_lessons": next_items,
        "review": [dict(r) for r in review],
        "streak": user["streak"],
        "points": user["points"],
    }