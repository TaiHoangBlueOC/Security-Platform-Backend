import uuid

from sqlalchemy import JSON, UUID, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

schema_name = "security_platform"
schema_args = {"schema": schema_name}


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = schema_args

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CaseModel(Base):
    __tablename__ = "cases"
    __table_args__ = schema_args

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey(f"{schema_name}.users.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EvidenceModel(Base):
    __tablename__ = "evidences"
    __table_args__ = schema_args

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID, ForeignKey(f"{schema_name}.cases.id"), nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MessageModel(Base):
    __tablename__ = "messages"
    __table_args__ = schema_args

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    evidence_id = Column(
        UUID, ForeignKey(f"{schema_name}.evidences.id"), nullable=False
    )
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    payload = Column(String, nullable=False)
    status = Column(String, nullable=False)
    embeddings = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
