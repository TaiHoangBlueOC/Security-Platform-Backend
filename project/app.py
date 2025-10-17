import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import settings
from project.presentation.api.authentication.authentication_routes import \
    router as auth_router
from project.presentation.api.case_management.case_management_routes import \
    router as case_management_router
from project.presentation.api.upload_evidences.upload_evidences_routes import \
    router as upload_evidences_router

logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the FastAPI server ...")
    logger.info(f"Service Title: {settings.fastapi.title}")
    logger.info(f"Service Version: {settings.fastapi.version}")
    logger.info(f"Service Description: {settings.fastapi.description}")


app = FastAPI(
    title=settings.fastapi.title,
    description=settings.fastapi.description,
    version=settings.fastapi.version,
    root_path=settings.fastapi.api_prefix,
    openapi_url=settings.fastapi.openapi_url,
    debug=settings.fastapi.debug,
    # lifespan=lifespan
)

origins = [
    "http://localhost:8081",
    "http://localhost:8099",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(auth_router)
app.include_router(case_management_router)
app.include_router(upload_evidences_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the FastAPI server ...")
    logger.info(f"Service Title: {settings.fastapi.title}")
    logger.info(f"Service Version: {settings.fastapi.version}")
    logger.info(f"Service Description: {settings.fastapi.description}")


if __name__ == "__main__":
    import asyncio

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    hypercorn_config = Config()
    hypercorn_config.bind = ["0.0.0.0:8099"]

    asyncio.run(serve(app, hypercorn_config))
