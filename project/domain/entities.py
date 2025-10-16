from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from project.domain.enums import EvidenceStatus


@dataclass
class UserEntity:
    id: UUID
    username: str
    hashed_password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class CaseEntity:
    id: UUID
    user_id: UUID
    title: str
    status: str
    description: str | None = None
    slug: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class EvidenceEntity:
    id: UUID
    case_id: UUID
    file_path: str
    status: EvidenceStatus
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class MessageEntity:
    id: UUID
    evidence_id: UUID
    sender: str
    receiver: str
    payload: str
    status: EvidenceStatus
    embeddings: list[float] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
