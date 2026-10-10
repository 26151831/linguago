"""认证依赖：从 Authorization 头解析当前登录用户。"""
from fastapi import Header, HTTPException

from . import database, security


def get_current_user(authorization: str = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录")
    token = authorization.removeprefix("Bearer ").strip()
    conn = database.get_connection()
    row = conn.execute(
        """
        SELECT u.id, u.username, u.email, u.native_language, u.target_languages,
               u.level, u.points, u.streak, u.last_activity_date, u.created_at
        FROM sessions s JOIN users u ON u.id = s.user_id
        WHERE s.token = ? AND s.expires_at > ?
        """,
        (token, security.now_iso()),
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    return dict(row)


def get_optional_user(authorization: str = Header(default=None)) -> dict | None:
    try:
        return get_current_user(authorization)
    except HTTPException:
        return None