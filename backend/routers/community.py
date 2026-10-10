"""社区：帖子、评论与点赞。"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .. import database, security
from ..deps import get_current_user
from .achievements import check_achievements

router = APIRouter(prefix="/api/posts", tags=["community"])

LANG_NAMES = {"en": "英语", "ja": "日语", "ko": "韩语", "all": "综合"}


class PostBody(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=3000)
    language: str = "all"


class CommentBody(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


def _post_payload(conn, post: dict, user_id: int) -> dict:
    author = conn.execute("SELECT id, username FROM users WHERE id = ?", (post["user_id"],)).fetchone()
    like_count = conn.execute("SELECT COUNT(*) AS c FROM post_likes WHERE post_id = ?", (post["id"],)).fetchone()["c"]
    comment_count = conn.execute("SELECT COUNT(*) AS c FROM comments WHERE post_id = ?", (post["id"],)).fetchone()["c"]
    liked = conn.execute(
        "SELECT 1 FROM post_likes WHERE post_id = ? AND user_id = ?", (post["id"], user_id)
    ).fetchone() is not None
    return {
        "id": post["id"],
        "title": post["title"],
        "content": post["content"],
        "language": post["language"],
        "language_name": LANG_NAMES.get(post["language"], post["language"]),
        "created_at": post["created_at"],
        "author_id": author["id"],
        "author": author["username"],
        "like_count": like_count,
        "comment_count": comment_count,
        "liked": liked,
    }


@router.get("")
def list_posts(language: str | None = None, user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    try:
        query = "SELECT * FROM posts"
        params: tuple = ()
        if language and language != "all":
            query += " WHERE language = ?"
            params = (language,)
        query += " ORDER BY id DESC LIMIT 100"
        rows = conn.execute(query, params).fetchall()
        return {"posts": [_post_payload(conn, dict(r), user["id"]) for r in rows]}
    finally:
        conn.close()


@router.post("")
def create_post(body: PostBody, user: dict = Depends(get_current_user)):
    post_id = database.execute(
        "INSERT INTO posts (user_id, title, content, language, created_at) VALUES (?,?,?,?,?)",
        (user["id"], body.title, body.content, body.language, security.now_iso()),
    )

    conn = database.get_connection()
    try:
        newly = check_achievements(conn, user["id"])
        conn.commit()
    finally:
        conn.close()

    return {"id": post_id, "new_achievements": [{"code": a["code"], "name": a["name"], "icon": a["icon"]} for a in newly]}


@router.get("/{post_id}")
def post_detail(post_id: int, user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    try:
        post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存在")
        payload = _post_payload(conn, dict(post), user["id"])
        comments = conn.execute(
            """
            SELECT c.*, u.username AS author
            FROM comments c JOIN users u ON u.id = c.user_id
            WHERE c.post_id = ? ORDER BY c.id
            """,
            (post_id,),
        ).fetchall()
        payload["comments"] = [dict(c) for c in comments]
        return payload
    finally:
        conn.close()


@router.post("/{post_id}/comments")
def add_comment(post_id: int, body: CommentBody, user: dict = Depends(get_current_user)):
    if not database.fetch_one("SELECT id FROM posts WHERE id = ?", (post_id,)):
        raise HTTPException(status_code=404, detail="帖子不存在")
    cid = database.execute(
        "INSERT INTO comments (post_id, user_id, content, created_at) VALUES (?,?,?,?)",
        (post_id, user["id"], body.content, security.now_iso()),
    )
    return {"id": cid, "author": user["username"], "content": body.content, "created_at": security.now_iso()}


@router.post("/{post_id}/like")
def toggle_like(post_id: int, user: dict = Depends(get_current_user)):
    if not database.fetch_one("SELECT id FROM posts WHERE id = ?", (post_id,)):
        raise HTTPException(status_code=404, detail="帖子不存在")
    conn = database.get_connection()
    existing = conn.execute(
        "SELECT 1 FROM post_likes WHERE post_id = ? AND user_id = ?", (post_id, user["id"])
    ).fetchone()
    if existing:
        conn.execute("DELETE FROM post_likes WHERE post_id = ? AND user_id = ?", (post_id, user["id"]))
        liked = False
    else:
        conn.execute("INSERT INTO post_likes (post_id, user_id) VALUES (?,?)", (post_id, user["id"]))
        liked = True
    conn.commit()
    like_count = conn.execute("SELECT COUNT(*) AS c FROM post_likes WHERE post_id = ?", (post_id,)).fetchone()["c"]
    conn.close()
    return {"liked": liked, "like_count": like_count}