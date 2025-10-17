from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from project.domain.enums import CaseStatus, EvidenceStatus, UserRole


@dataclass
class UserEntity:
    id: UUID
    username: str
    hashed_password: str
    role: UserRole
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class CaseEntity:
    id: UUID
    user_id: UUID
    title: str
    status: CaseStatus
    description: str | None = None
    slug: str | None = None
    summary: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class EvidenceEntity:
    id: UUID
    case_id: UUID
    source: str
    status: EvidenceStatus
    format: str
    metadata: Dict[str, Any]
    attributes: list[str]
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


@dataclass
class CaseGroupEntity:
    id: UUID
    title: str
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class CaseGroupAssociationEntity:
    id: UUID
    case_id: UUID
    group_id: UUID
    created_at: datetime | None = None


@dataclass
class ProfileEntity:
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class UserGroupEntity:
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class UserGroupAssociationEntity:
    id: UUID
    user_id: UUID
    group_id: UUID
    created_at: datetime | None = None


@dataclass
class SharedCaseUserEntity:
    id: UUID
    case_id: UUID
    user_id: UUID
    created_at: datetime | None = None


@dataclass
class SharedCaseGroupEntity:
    id: UUID
    case_id: UUID
    group_id: UUID
    created_at: datetime | None = None
