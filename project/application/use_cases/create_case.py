import uuid

from project.application.interfaces.case_repository_interface import \
    ICaseRepository
from project.domain.entities import CaseEntity, UserEntity
from project.domain.enums import CaseStatus


class CreateCaseUseCase:
    def __init__(self, file_repo: ICaseRepository):
        self.file_repo = file_repo

    async def execute(
        self, title: str, description: str, slug: str, user: UserEntity
    ) -> CaseEntity:
        case_entity = CaseEntity(
            id=uuid.uuid4(),
            user_id=user.id,
            title=title,
            status=CaseStatus.OPEN,
            description=description,
            slug=slug,
        )

        return await self.file_repo.create_case(case_entity)
