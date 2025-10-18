import os, jwt
from datetime import datetime, timedelta, timezone


JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def issue_reset_token(user_id: int, minutes: int = 15) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=minutes)
    payload = {"sub": f"reset:{user_id}", "exp": int(exp.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def parse_reset_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        sub = payload.get("sub", "")
        if not sub.startswith("reset:"):
            return None
        return int(sub.split(":", 1)[1])
    except Exception:
        return None