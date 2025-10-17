from typing import Callable

from fastapi import Depends

from project.dependencies.database_dependency import get_async_db, get_sync_db
from project.infrastructure.repositories.case_repository import CaseRepository
from project.infrastructure.repositories.evidence_repository import \
    EvidenceRepository
from project.infrastructure.repositories.user_repository import UserRepository


def get_user_repo(async_mode: bool = True) -> Callable:
    async def _get_user_repo(db=Depends(get_async_db if async_mode else get_sync_db)):
        return UserRepository(db)

    return _get_user_repo


def get_case_repo(async_mode: bool = True) -> Callable:
    async def _get_case_repo(db=Depends(get_async_db if async_mode else get_sync_db)):
        return CaseRepository(db)

    return _get_case_repo


def get_evidence_repo(async_mode: bool = True) -> Callable:
    async def _get_evidence_repo(
        db=Depends(get_async_db if async_mode else get_sync_db),
    ):
        return EvidenceRepository(db)

    return _get_evidence_repo
