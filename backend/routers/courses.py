"""课程与课程列表。"""
import json

from fastapi import APIRouter, Depends, HTTPException

from .. import database
from ..deps import get_optional_user

router = APIRouter(prefix="/api", tags=["courses"])

LANGUAGES = [
    {"code": "en", "name": "英语", "flag": "🇺🇸", "native": "English"},
    {"code": "ja", "name": "日语", "flag": "🇯🇵", "native": "日本語"},
    {"code": "ko", "name": "韩语", "flag": "🇰🇷", "native": "한국어"},
]


@router.get("/languages")
def list_languages():
    return LANGUAGES


def _lesson_payload(lesson: dict) -> dict:
    content = lesson["content"]
    if isinstance(content, str):
        content = json.loads(content)
    return {
        "id": lesson["id"],
        "course_id": lesson["course_id"],
        "title": lesson["title"],
        "type": lesson["type"],
        "content": content,
        "order_index": lesson["order_index"],
    }


@router.get("/courses")
def list_courses(language: str | None = None, user: dict | None = Depends(get_optional_user)):
    query = "SELECT * FROM courses"
    params: tuple = ()
    if language:
        query += " WHERE language = ?"
        params = (language,)
    query += " ORDER BY order_index"
    courses = database.fetch_all(query, params)

    completed_map = {}
    if user:
        rows = database.fetch_all(
            """
            SELECT l.course_id, COUNT(*) AS done
            FROM lesson_progress p JOIN lessons l ON l.id = p.lesson_id
            WHERE p.user_id = ? GROUP BY l.course_id
            """,
            (user["id"],),
        )
        completed_map = {r["course_id"]: r["done"] for r in rows}

    total_map = {}
    for c in courses:
        total_map[c["id"]] = database.fetch_one("SELECT COUNT(*) AS c FROM lessons WHERE course_id = ?", (c["id"],))["c"]

    result = []
    for c in courses:
        result.append({
            **c,
            "total_lessons": total_map.get(c["id"], 0),
            "completed_lessons": completed_map.get(c["id"], 0),
        })
    return result


@router.get("/courses/{course_id}")
def course_detail(course_id: int, user: dict | None = Depends(get_optional_user)):
    course = database.fetch_one("SELECT * FROM courses WHERE id = ?", (course_id,))
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    lessons = database.fetch_all("SELECT * FROM lessons WHERE course_id = ? ORDER BY order_index", (course_id,))

    completed = set()
    if user:
        rows = database.fetch_all(
            "SELECT lesson_id FROM lesson_progress WHERE user_id = ? AND lesson_id IN (SELECT id FROM lessons WHERE course_id = ?)",
            (user["id"], course_id),
        )
        completed = {r["lesson_id"] for r in rows}

    payload_lessons = []
    for l in lessons:
        pl = _lesson_payload(l)
        pl["completed"] = l["id"] in completed
        payload_lessons.append(pl)

    return {
        **course,
        "total_lessons": len(lessons),
        "completed_lessons": len([x for x in payload_lessons if x["completed"]]),
        "lessons": payload_lessons,
    }


@router.get("/lessons/{lesson_id}")
def lesson_detail(lesson_id: int):
    lesson = database.fetch_one("SELECT * FROM lessons WHERE id = ?", (lesson_id,))
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    course = database.fetch_one("SELECT * FROM courses WHERE id = ?", (lesson["course_id"],))
    return {**_lesson_payload(lesson), "course": course}