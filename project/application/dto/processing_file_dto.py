from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateCaseRequest(BaseModel):
    title: str
    description: str | None = None
    slug: str | None = None
    summary: str | None = None


class CaseEvidenceResponse(BaseModel):
    id: UUID
    source: str
    status: str
    format: str
    metadata: dict
    attributes: list[str]
    created_at: datetime
    updated_at: datetime | None = None


class CaseResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None = None
    slug: str | None = None
    status: str
    summary: str | None = None
    evidences: list[CaseEvidenceResponse] = []
    created_at: datetime
    updated_at: datetime | None = None
