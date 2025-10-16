from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateCaseRequest(BaseModel):
    title: str
    description: str | None = None
    slug: str | None = None


class CreateCaseResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    slug: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime | None = None
