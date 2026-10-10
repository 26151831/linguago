"""成就系统：解锁检测与查询。"""
from fastapi import APIRouter, Depends

from .. import database, security
from ..deps import get_current_user

router = APIRouter(prefix="/api/achievements", tags=["achievements"])


def _stats(conn, user_id: int) -> dict:
    lessons = conn.execute(
        "SELECT COUNT(*) AS c FROM lesson_progress WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    streak = conn.execute("SELECT streak FROM users WHERE id = ?", (user_id,)).fetchone()["streak"]
    points = conn.execute("SELECT points FROM users WHERE id = ?", (user_id,)).fetchone()["points"]
    langs = conn.execute(
        """
        SELECT COUNT(DISTINCT c.language) AS c
        FROM lesson_progress p JOIN lessons l ON l.id = p.lesson_id JOIN courses c ON c.id = l.course_id
        WHERE p.user_id = ?
        """,
        (user_id,),
    ).fetchone()["c"]
    posts = conn.execute("SELECT COUNT(*) AS c FROM posts WHERE user_id = ?", (user_id,)).fetchone()["c"]
    return {"lessons_completed": lessons, "streak": streak, "points": points, "languages": langs, "posts": posts}


def check_achievements(conn, user_id: int) -> list[dict]:
    """根据当前统计解锁新成就，返回本次新解锁的成就列表。"""
    stats = _stats(conn, user_id)
    rows = conn.execute("SELECT * FROM achievements").fetchall()
    newly = []
    for a in rows:
        a = dict(a)
        cur = stats.get(a["condition_type"], 0)
        if cur >= a["condition_value"]:
            exists = conn.execute(
                "SELECT 1 FROM user_achievements WHERE user_id = ? AND achievement_id = ?",
                (user_id, a["id"]),
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO user_achievements (user_id, achievement_id, unlocked_at) VALUES (?,?,?)",
                    (user_id, a["id"], security.now_iso()),
                )
                newly.append(a)
    return newly


@router.get("")
def list_achievements(user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    try:
        check_achievements(conn, user["id"])
        rows = conn.execute("SELECT * FROM achievements ORDER BY id").fetchall()
        unlocked = {
            r["achievement_id"]: r["unlocked_at"]
            for r in conn.execute(
                "SELECT achievement_id, unlocked_at FROM user_achievements WHERE user_id = ?", (user["id"],)
            ).fetchall()
        }
        conn.commit()
    finally:
        conn.close()

    result = []
    for a in rows:
        a = dict(a)
        result.append({**a, "unlocked": a["id"] in unlocked, "unlocked_at": unlocked.get(a["id"])})
    return {"achievements": result, "unlocked_count": sum(1 for x in result if x["unlocked"])}