import uuid

from project.application.dto.processing_file_dto import (CaseResponse,
                                                         CreateCaseRequest)
from project.application.interfaces.case_repository_interface import \
    ICaseRepository
from project.domain.entities import CaseEntity
from project.domain.enums import CaseStatus


class CreateCaseUseCase:
    def __init__(self, file_repo: ICaseRepository):
        self.file_repo = file_repo

    async def execute(
        self, case_request: CreateCaseRequest, user_id: uuid.UUID
    ) -> CaseResponse:

        case_entity = CaseEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            title=case_request.title,
            status=CaseStatus.OPEN,
            description=case_request.description,
            slug=case_request.slug,
        )

        return await self.file_repo.create_case(case_entity)
