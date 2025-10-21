import uuid

from sqlalchemy import JSON, UUID, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import backref, declarative_base, declarative_mixin, relationship

from project.domain.enums import UserRole

Base = declarative_base()

schema_name = "security_platform"
schema_args = {"schema": schema_name}


@declarative_mixin
class CommonModelMixin:
    """Shared base fields for all models."""

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserModel(CommonModelMixin, Base):
    __tablename__ = "users"
    __table_args__ = schema_args

    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=UserRole.USER)

    profile = relationship(
        "ProfileModel", uselist=False, backref=backref("user", uselist=False)
    )


class ProfileModel(CommonModelMixin, Base):
    __tablename__ = "profiles"
    __table_args__ = schema_args

    user_id = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class CaseModel(CommonModelMixin, Base):
    __tablename__ = "cases"
    __table_args__ = schema_args

    user_id = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    summary = Column(String, nullable=True)

    evidences = relationship(
        "EvidenceModel", backref="case", cascade="all, delete-orphan"
    )

    collections = relationship(
        "CollectionModel",
        secondary=f"{schema_name}.case_collection_associations",
        back_populates="cases",
    )


class EvidenceModel(CommonModelMixin, Base):
    __tablename__ = "evidences"
    __table_args__ = schema_args

    case_id = Column(UUID, ForeignKey(f"{schema_name}.cases.id"), nullable=False)
    source = Column(String, nullable=False)
    format = Column(String, nullable=False)
    status = Column(String, nullable=False)
    metadata_json = Column("metadata", JSONB, nullable=True)
    attributes = Column(ARRAY(String), nullable=True)


class MessageModel(CommonModelMixin, Base):
    __tablename__ = "messages"
    __table_args__ = schema_args

    evidence_id = Column(
        UUID, ForeignKey(f"{schema_name}.evidences.id"), nullable=False
    )
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    payload = Column(String, nullable=False)
    status = Column(String, nullable=False)
    embeddings = Column(JSON, nullable=True)


class CollectionModel(CommonModelMixin, Base):
    __tablename__ = "collections"
    __table_args__ = schema_args

    user_id = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    cases = relationship(
        "CaseModel",
        secondary=f"{schema_name}.case_collection_associations",
    )


class CaseCollectionAssociationModel(CommonModelMixin, Base):
    __tablename__ = "case_collection_associations"
    __table_args__ = schema_args

    case_id = Column(UUID, ForeignKey(f"{schema_name}.cases.id"), nullable=False)
    collection_id = Column(
        UUID, ForeignKey(f"{schema_name}.collections.id"), nullable=False
    )


class GroupModel(CommonModelMixin, Base):
    __tablename__ = "groups"
    __table_args__ = schema_args

    name = Column(String, nullable=False)
    created_by = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)

    members = relationship(
        "UserModel",
        secondary=f"{schema_name}.user_group_associations",
    )


class UserGroupAssociationModel(CommonModelMixin, Base):
    __tablename__ = "user_group_associations"
    __table_args__ = schema_args

    user_id = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)
    group_id = Column(UUID, ForeignKey(f"{schema_name}.groups.id"), nullable=False)


class SharedCaseUserModel(CommonModelMixin, Base):
    __tablename__ = "shared_case_users"
    __table_args__ = schema_args

    case_id = Column(UUID, ForeignKey(f"{schema_name}.cases.id"), nullable=False)
    user_id = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)


class SharedCaseGroupModel(CommonModelMixin, Base):
    __tablename__ = "shared_case_groups"
    __table_args__ = schema_args

    case_id = Column(UUID, ForeignKey(f"{schema_name}.cases.id"), nullable=False)
    group_id = Column(UUID, ForeignKey(f"{schema_name}.groups.id"), nullable=False)
