from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserEntity:
    id: UUID
    username: str
    hashed_password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
