from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from project.application.exceptions.JWTException import JWTDecodeError
from project.core.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        return payload
    except JWTError as e:
        raise JWTDecodeError("Invalid or expired token") from e
