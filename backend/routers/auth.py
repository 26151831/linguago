"""注册、登录、个人信息。"""
import datetime
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from .. import database, security
from ..deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

TOKEN_DAYS = 30


class RegisterBody(BaseModel):
    username: str = Field(min_length=2, max_length=24)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
    native_language: str = "zh"
    target_languages: list[str] = ["en"]
    level: str = "A1"


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class ProfileBody(BaseModel):
    native_language: str = "zh"
    target_languages: list[str] = ["en"]
    level: str = "A1"


def _public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "native_language": user["native_language"],
        "target_languages": json.loads(user["target_languages"] or "[]"),
        "level": user["level"],
        "points": user["points"],
        "streak": user["streak"],
        "created_at": user["created_at"],
    }


def _create_session(user_id: int) -> str:
    token = security.generate_token()
    created = security.now_iso()
    expires = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=TOKEN_DAYS)).isoformat()
    database.execute("INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?,?,?,?)", (token, user_id, created, expires))
    return token


@router.post("/register")
def register(body: RegisterBody):
    email = body.email.lower()
    if database.fetch_one("SELECT id FROM users WHERE email = ?", (email,)):
        raise HTTPException(status_code=409, detail="该邮箱已被注册")
    if database.fetch_one("SELECT id FROM users WHERE username = ?", (body.username,)):
        raise HTTPException(status_code=409, detail="该用户名已被占用")

    user_id = database.execute(
        "INSERT INTO users (username, email, password_hash, native_language, target_languages, level, created_at) VALUES (?,?,?,?,?,?,?)",
        (
            body.username,
            email,
            security.hash_password(body.password),
            body.native_language,
            json.dumps(body.target_languages, ensure_ascii=False),
            body.level,
            security.now_iso(),
        ),
    )
    token = _create_session(user_id)
    user = database.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    return {"token": token, "user": _public_user(user)}


@router.post("/login")
def login(body: LoginBody):
    user = database.fetch_one("SELECT * FROM users WHERE email = ?", (body.email.lower(),))
    if not user or not security.verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    token = _create_session(user["id"])
    return {"token": token, "user": _public_user(user)}


@router.post("/logout")
def logout(user: dict = Depends(get_current_user)):
    # 通过 token 登出由前端删除；这里清理该用户所有会话以保证安全
    conn = database.get_connection()
    conn.execute("DELETE FROM sessions WHERE user_id = ?", (user["id"],))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return _public_user(user)


@router.put("/profile")
def update_profile(body: ProfileBody, user: dict = Depends(get_current_user)):
    database.execute(
        "UPDATE users SET native_language = ?, target_languages = ?, level = ? WHERE id = ?",
        (body.native_language, json.dumps(body.target_languages, ensure_ascii=False), body.level, user["id"]),
    )
    updated = database.fetch_one("SELECT * FROM users WHERE id = ?", (user["id"],))
    return _public_user(updated)