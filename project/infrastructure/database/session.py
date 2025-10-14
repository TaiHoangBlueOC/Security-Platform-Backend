from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from runtime_settings import (
    SECURITY_PLATFORM_POSTGRES_DATABASE,
    SECURITY_PLATFORM_POSTGRES_HOST,
    SECURITY_PLATFORM_POSTGRES_PASSWORD,
    SECURITY_PLATFORM_POSTGRES_PORT,
    SECURITY_PLATFORM_POSTGRES_USER_NAME,
)

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{SECURITY_PLATFORM_POSTGRES_USER_NAME}:{SECURITY_PLATFORM_POSTGRES_PASSWORD}@"
    f"{SECURITY_PLATFORM_POSTGRES_HOST}:{SECURITY_PLATFORM_POSTGRES_PORT}/"
    f"{SECURITY_PLATFORM_POSTGRES_DATABASE}"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
