import uuid
from datetime import datetime

from pydantic import BaseModel

from project.domain.enums import UserRole


class RegisterRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime | None = None


class UserInternal(UserResponse):
    role: UserRole
    hashed_password: str
