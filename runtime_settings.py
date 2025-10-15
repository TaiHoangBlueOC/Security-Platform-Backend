import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Database Configuration ---
SECURITY_PLATFORM_POSTGRES_HOST = os.getenv("SECURITY_PLATFORM_POSTGRES_HOST")
SECURITY_PLATFORM_POSTGRES_PORT = os.getenv("SECURITY_PLATFORM_POSTGRES_PORT")
SECURITY_PLATFORM_POSTGRES_DATABASE = os.getenv("SECURITY_PLATFORM_POSTGRES_DATABASE")
SECURITY_PLATFORM_POSTGRES_USER_NAME = os.getenv("SECURITY_PLATFORM_POSTGRES_USER_NAME")
SECURITY_PLATFORM_POSTGRES_PASSWORD = os.getenv("SECURITY_PLATFORM_POSTGRES_PASSWORD")

# --- JWT / Auth Configuration ---
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# --- FastAPI Configuration ---
FASTAPI_TITLE = os.getenv("FASTAPI_TITLE", "Security Platform API")
FASTAPI_VERSION = os.getenv("FASTAPI_VERSION", "0.1.0")
FASTAPI_DESCRIPTION = os.getenv(
    "FASTAPI_DESCRIPTION", "Security Platform backend service."
)
FASTAPI_DEBUG = os.getenv("FASTAPI_DEBUG", "false").lower() == "true"
FASTAPI_DOCS_URL = os.getenv("FASTAPI_DOCS_URL", "/docs")
FASTAPI_REDOC_URL = os.getenv("FASTAPI_REDOC_URL", "/redoc")
FASTAPI_OPENAPI_URL = os.getenv("FASTAPI_OPENAPI_URL", "/openapi.json")
FASTAPI_API_PREFIX = os.getenv("FASTAPI_API_PREFIX", "/api/v1")

# --- Application Info ---
APP_NAME = os.getenv("APP_NAME", "Security Platform")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
