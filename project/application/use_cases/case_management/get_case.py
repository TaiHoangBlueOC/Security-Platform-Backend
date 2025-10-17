from uuid import UUID

from project.application.interfaces.case_repository_interface import \
    ICaseRepository
from project.domain.entities import CaseEntity


class GetCaseUseCase:
    def __init__(self, case_repo: ICaseRepository):
        self.case_repo = case_repo

    async def execute(self, case_id: UUID, user_id: UUID) -> CaseEntity:
        return await self.case_repo.get_case_by_id(case_id, user_id)


class GetCasesByUserUseCase:
    def __init__(self, case_repo: ICaseRepository):
        self.case_repo = case_repo

    async def execute(self, user_id: UUID) -> list[CaseEntity]:
        return await self.case_repo.get_cases_by_user(user_id)
