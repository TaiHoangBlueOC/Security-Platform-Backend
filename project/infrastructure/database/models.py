import uuid

from sqlalchemy import UUID, Column, DateTime, String, func

from project.infrastructure.database.session import Base

schema_name = "security_platform"
schema_args = {"schema": schema_name}


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
