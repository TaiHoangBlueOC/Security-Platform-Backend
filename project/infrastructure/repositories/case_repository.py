from typing import List

from sqlalchemy import select

from project.application.interfaces.process_file_repository_interface import (
    ICaseRepository,
)
from project.domain.entities import CaseEntity
from project.infrastructure.database.models import CaseModel


class CaseRepository(ICaseRepository):
    def __init__(self, session):
        self.session = session

    async def create_case(self, case: CaseEntity) -> CaseEntity:
        db_case = CaseModel(
            user_id=case.user_id,
            title=case.title,
            status=case.status,
            description=case.description,
            slug=case.slug,
        )
        self.session.add(db_case)
        await self.session.commit()
        await self.session.refresh(db_case)

        case.id = db_case.id
        case.created_at = db_case.created_at
        case.updated_at = db_case.updated_at
        return case

    async def get_cases_by_user(self, user_id: str) -> List[CaseEntity]:
        stmt = select(CaseModel).where(CaseModel.user_id == user_id)
        result = await self.session.execute(stmt)
        cases = result.scalars().all()
        return [
            CaseEntity(
                id=db_case.id,
                user_id=db_case.user_id,
                title=db_case.title,
                status=db_case.status,
                description=db_case.description,
                slug=db_case.slug,
                created_at=db_case.created_at,
                updated_at=db_case.updated_at,
            )
            for db_case in cases
        ]
