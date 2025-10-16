from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from project.core.config import (SECURITY_PLATFORM_POSTGRES_DATABASE,
                                 SECURITY_PLATFORM_POSTGRES_HOST,
                                 SECURITY_PLATFORM_POSTGRES_PASSWORD,
                                 SECURITY_PLATFORM_POSTGRES_PORT,
                                 SECURITY_PLATFORM_POSTGRES_USER_NAME)

DATABASE_ASYNC_URL = (
    f"postgresql+asyncpg://"
    f"{SECURITY_PLATFORM_POSTGRES_USER_NAME}:{SECURITY_PLATFORM_POSTGRES_PASSWORD}@"
    f"{SECURITY_PLATFORM_POSTGRES_HOST}:{SECURITY_PLATFORM_POSTGRES_PORT}/"
    f"{SECURITY_PLATFORM_POSTGRES_DATABASE}"
)

DATABASE_SYNC_URL = (
    f"postgresql+psycopg2://"
    f"{SECURITY_PLATFORM_POSTGRES_USER_NAME}:{SECURITY_PLATFORM_POSTGRES_PASSWORD}@"
    f"{SECURITY_PLATFORM_POSTGRES_HOST}:{SECURITY_PLATFORM_POSTGRES_PORT}/"
    f"{SECURITY_PLATFORM_POSTGRES_DATABASE}"
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


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
