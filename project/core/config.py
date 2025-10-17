import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load .env once globally
load_dotenv()


# --- Database Configuration ---
@dataclass(frozen=True)
class DatabaseConfig:
    type: str = os.getenv("SECURITY_PLATFORM_DATABASE_TYPE", "postgresql")
    host: str = os.getenv("SECURITY_PLATFORM_DATABASE_HOST", "localhost")
    port: int = int(os.getenv("SECURITY_PLATFORM_DATABASE_PORT", 5432))
    database: str = os.getenv("SECURITY_PLATFORM_DATABASE_NAME", "security_platform")
    username: str = os.getenv("SECURITY_PLATFORM_DATABASE_USER_NAME", "postgres")
    password: str = os.getenv("SECURITY_PLATFORM_DATABASE_PASSWORD", "password123!")
    sync_driver: str = os.getenv("SECURITY_PLATFORM_DATABASE_SYNC_DRIVER", "psycopg2")
    async_driver: str = os.getenv("SECURITY_PLATFORM_DATABASE_ASYNC_DRIVER", "asyncpg")


# --- JWT / Auth Configuration ---
@dataclass(frozen=True)
class JWTConfig:
    secret_key: str = os.getenv("JWT_SECRET_KEY", "secret")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )


# --- FastAPI Configuration ---
@dataclass(frozen=True)
class FastAPIConfig:
    title: str = os.getenv("FASTAPI_TITLE", "Security Platform API")
    version: str = os.getenv("FASTAPI_VERSION", "0.1.0")
    description: str = os.getenv(
        "FASTAPI_DESCRIPTION", "Security Platform backend service."
    )
    debug: bool = os.getenv("FASTAPI_DEBUG", "false").lower() == "true"
    docs_url: str = os.getenv("FASTAPI_DOCS_URL", "/docs")
    redoc_url: str = os.getenv("FASTAPI_REDOC_URL", "/redoc")
    openapi_url: str = os.getenv("FASTAPI_OPENAPI_URL", "/openapi.json")
    api_prefix: str = os.getenv("FASTAPI_API_PREFIX", "/api/v1")


# --- Application Info ---
@dataclass(frozen=True)
class AppInfo:
    name: str = os.getenv("APP_NAME", "Security Platform")
    version: str = os.getenv("APP_VERSION", "0.1.0")
    debug: bool = os.getenv("APP_DEBUG", "false").lower() == "true"


# --- Evidence Configuration ---
@dataclass(frozen=True)
class EvidenceConfig:
    upload_directory: str = os.getenv("UPLOAD_DIRECTORY", ".uploads")

    def __post_init__(self):
        os.makedirs(self.upload_directory, exist_ok=True)


# --- Celery Configuration ---
@dataclass(frozen=True)
class CeleryConfig:
    name: str = os.getenv("CELERY_NAME", "security_platform_worker")
    broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")


# --- Main Configuration Container ---
@dataclass(frozen=True)
class Settings:
    database: DatabaseConfig = DatabaseConfig()
    jwt: JWTConfig = JWTConfig()
    fastapi: FastAPIConfig = FastAPIConfig()
    app: AppInfo = AppInfo()
    evidence: EvidenceConfig = EvidenceConfig()
    celery: CeleryConfig = CeleryConfig()


# Shared global instance
settings = Settings()
