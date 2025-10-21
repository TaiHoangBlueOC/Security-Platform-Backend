from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from project.domain.enums import CaseStatus, EvidenceStatus, UserRole


@dataclass
class ProfileEntity:
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserEntity:
    id: UUID
    username: str
    hashed_password: str
    role: UserRole
    profile: ProfileEntity = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class EvidenceEntity:
    id: UUID
    case_id: UUID
    source: str
    status: EvidenceStatus
    format: str
    metadata: Dict[str, Any]
    attributes: List[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CaseEntity:
    id: UUID
    user_id: UUID
    title: str
    status: CaseStatus
    description: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    evidences: List[EvidenceEntity] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class MessageEntity:
    id: UUID
    evidence_id: UUID
    sender: str
    receiver: str
    payload: str
    status: EvidenceStatus
    embeddings: List[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CollectionEntity:
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    cases: List[CaseEntity] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CaseCollectionAssociationEntity:
    id: UUID
    case_id: UUID
    group_id: UUID
    created_at: Optional[datetime] = None


@dataclass
class GroupEntity:
    id: UUID
    name: str
    created_by: UUID
    members: List[UserEntity] = field(default_factory=list)
    cases: List[CaseEntity] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserGroupAssociationEntity:
    id: UUID
    user_id: UUID
    group_id: UUID
    created_at: Optional[datetime] = None


@dataclass
class SharedCaseUserEntity:
    id: UUID
    case_id: UUID
    user_id: UUID
    created_at: Optional[datetime] = None


@dataclass
class SharedCaseGroupEntity:
    id: UUID
    case_id: UUID
    group_id: UUID
    created_at: Optional[datetime] = None
