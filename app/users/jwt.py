from datetime import datetime, timedelta, timezone

import jwt

from app.core.settings import Settings


settings = Settings()   # type: ignore[call-arg]
ALGORITHM = "HS256"

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth.jwt_expired_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.auth.jwt_secret, algorithm=ALGORITHM)

def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.auth.jwt_secret, algorithm=ALGORITHM)
        return int(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        return None
