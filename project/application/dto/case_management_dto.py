from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class CreateCaseRequest(BaseModel):
    title: str
    description: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None


class UpdateCaseRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None


class CreateCaseCollectionRequest(BaseModel):
    title: str
    description: Optional[str] = None


class UpdateCaseCollectionRequest(BaseModel):
    title: str
    description: Optional[str] = None


class CaseEvidenceResponse(BaseModel):
    id: UUID
    source: str
    status: str
    format: str
    metadata: dict
    attributes: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None


class CaseResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    slug: Optional[str] = None
    status: str
    summary: Optional[str] = None
    evidences: List[CaseEvidenceResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None


class CollectionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    cases: List[CaseResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
