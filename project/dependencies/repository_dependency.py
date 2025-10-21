from fastapi import Depends

from project.application.interfaces.case_repository_interface import ICaseRepository
from project.application.interfaces.evidence_repository_interface import (
    IEvidenceRepository,
)
from project.application.interfaces.group_repository_interface import IGroupRepository
from project.application.interfaces.user_repository_interface import IUserRepository
from project.dependencies.database_dependency import get_async_db
from project.infrastructure.repositories.case_repository import CaseRepository
from project.infrastructure.repositories.evidence_repository import EvidenceRepository
from project.infrastructure.repositories.group_repository import GroupRepository
from project.infrastructure.repositories.user_repository import UserRepository


async def get_user_repo(db=Depends(get_async_db)) -> IUserRepository:
    return UserRepository(db)


async def get_case_repo(db=Depends(get_async_db)) -> ICaseRepository:
    return CaseRepository(db)


async def get_evidence_repo(db=Depends(get_async_db)) -> IEvidenceRepository:
    return EvidenceRepository(db)


async def get_group_repo(db=Depends(get_async_db)) -> IGroupRepository:
    return GroupRepository(db)
