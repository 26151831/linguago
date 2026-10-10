"""密码哈希、令牌生成与时间工具。"""
import datetime
import hashlib
import secrets


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def today_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def hash_password(password: str, salt: str | None = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 120_000)
    return f"{salt}:{dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, expected = stored.split(":", 1)
    except ValueError:
        return False
    actual = hash_password(password, salt).split(":", 1)[1]
    return secrets.compare_digest(actual, expected)


def generate_token() -> str:
    return secrets.token_hex(32)