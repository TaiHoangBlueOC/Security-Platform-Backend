import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import (FASTAPI_API_PREFIX, FASTAPI_DEBUG,
                                 FASTAPI_DESCRIPTION, FASTAPI_OPENAPI_URL,
                                 FASTAPI_TITLE, FASTAPI_VERSION)
from project.presentation.api.authentication.authentication_routes import \
    router as auth_router
from project.presentation.api.case_management.case_management_routes import \
    router as case_management_router
from project.presentation.api.upload_evidences.upload_evidences_routes import \
    router as upload_evidences_router

logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=FASTAPI_TITLE,
    description=FASTAPI_DESCRIPTION,
    version=FASTAPI_VERSION,
    root_path=FASTAPI_API_PREFIX,
    openapi_url=FASTAPI_OPENAPI_URL,
    debug=FASTAPI_DEBUG,
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
    logger.info(f"Service Title: {FASTAPI_TITLE}")
    logger.info(f"Service Version: {FASTAPI_VERSION}")
    logger.info(f"Service Description: {FASTAPI_DESCRIPTION}")


if __name__ == "__main__":
    import asyncio

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    hypercorn_config = Config()
    hypercorn_config.bind = ["0.0.0.0:8099"]

    asyncio.run(serve(app, hypercorn_config))
