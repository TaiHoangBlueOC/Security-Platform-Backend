from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from project.application.exceptions.JWTException import JWTDecodeError
from project.core.config import (ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM,
                                 JWT_SECRET_KEY)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTDecodeError("Invalid or expired token") from e
