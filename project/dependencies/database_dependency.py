from project.application.interfaces.file_storage_interface import IFileStorage
from project.application.interfaces.job_dispatcher_interface import \
    IJobDispatcher
from project.infrastructure.celery_tasks.celery_app import CeleryJobDispatcher
from project.infrastructure.database.session import (AsyncSessionLocal,
                                                     SessionLocal)
from project.infrastructure.file_storage.local_storage_service import \
    LocalFileStorage


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_file_storage() -> IFileStorage:
    return LocalFileStorage()


def get_job_dispatcher() -> IJobDispatcher:
    return CeleryJobDispatcher()
