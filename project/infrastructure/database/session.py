from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from project.core.config import settings

DATABASE_ASYNC_URL = (
    f"{settings.database.type}+{settings.database.async_driver}://"
    f"{settings.database.username}:{settings.database.password}@"
    f"{settings.database.host}:{settings.database.port}/"
    f"{settings.database.database}"
)

DATABASE_SYNC_URL = (
    f"{settings.database.type}+{settings.database.sync_driver}://"
    f"{settings.database.username}:{settings.database.password}@"
    f"{settings.database.host}:{settings.database.port}/"
    f"{settings.database.database}"
)

# Create engine
async_engine = create_async_engine(DATABASE_ASYNC_URL, echo=False, future=True)
sync_engine = create_engine(DATABASE_SYNC_URL, echo=False, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
