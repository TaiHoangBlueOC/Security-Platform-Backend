from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from project.application.dto.processing_file_dto import (CaseEvidenceResponse,
                                                         CaseResponse)
from project.application.interfaces.case_repository_interface import \
    ICaseRepository
from project.domain.entities import CaseEntity
from project.infrastructure.database.models import (CaseModel, EvidenceModel,
                                                    SharedCaseUserModel)


class CaseRepository(ICaseRepository):

    def __init__(self, session):
        self.session = session

    def _generate_case_response(
        self, case_model: CaseModel, evidences: EvidenceModel
    ) -> CaseResponse:
        return CaseResponse(
            id=case_model.id,
            user_id=case_model.user_id,
            title=case_model.title,
            status=case_model.status,
            description=case_model.description,
            slug=case_model.slug,
            summary=case_model.summary,
            evidences=[
                CaseEvidenceResponse(
                    id=evidence.id,
                    source=evidence.file_path,
                    status=evidence.status,
                    format=(
                        evidence.metadata.get("format", "") if evidence.metadata else ""
                    ),
                    metadata=evidence.metadata if evidence.metadata else {},
                    attributes=(
                        evidence.metadata.get("attributes", [])
                        if evidence.metadata
                        else []
                    ),
                    created_at=evidence.created_at,
                    updated_at=evidence.updated_at,
                )
                for evidence in evidences
            ],
            created_at=case_model.created_at,
            updated_at=case_model.updated_at,
        )

    async def create_case(self, case: CaseEntity) -> CaseEntity:
        db_case = CaseModel(
            id=case.id,
            user_id=case.user_id,
            title=case.title,
            status=case.status,
            description=case.description,
            slug=case.slug,
        )

        self.session.add(db_case)
        await self.session.commit()
        await self.session.refresh(db_case)

        # Create view permission for the case owner
        shared_relationships = SharedCaseUserModel(
            case_id=case.id, user_id=case.user_id
        )
        self.session.add(shared_relationships)
        await self.session.commit()

        return self._generate_case_response(db_case, [])

    async def get_case_by_id(self, case_id: UUID, user_id: UUID) -> CaseResponse | None:
        # Check if user has access to the case
        stmt = (
            select(SharedCaseUserModel)
            .where(SharedCaseUserModel.user_id == user_id)
            .where(SharedCaseUserModel.case_id == case_id)
        )
        result = await self.session.execute(stmt)
        shared_case = result.scalars().first()
        if not shared_case:
            return None

        # Fetch the case
        stmt = (
            select(CaseModel)
            .where(CaseModel.id == case_id)
            .options(joinedload(CaseModel.evidences))
        )
        result = await self.session.execute(stmt)
        db_case = result.scalars().first()
        if not db_case:
            return None

        return self._generate_case_response(db_case, db_case.evidences)

    async def get_cases_by_user(self, user_id: UUID) -> List[CaseResponse]:
        stmt = (
            select(CaseModel)
            .where(CaseModel.user_id == user_id)
            .options(joinedload(CaseModel.evidences))
        )
        result = await self.session.execute(stmt)
        cases = result.scalars().all()
        return [
            self._generate_case_response(db_case, db_case.evidences)
            for db_case in cases
        ]
