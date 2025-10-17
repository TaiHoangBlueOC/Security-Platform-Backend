from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from project.application.dto.processing_file_dto import CaseResponse
from project.domain.entities import CaseEntity


class ICaseRepository(ABC):
    @abstractmethod
    async def create_case(self, case: CaseEntity) -> CaseResponse:
        pass

    @abstractmethod
    async def get_cases_by_user(self, user_id: UUID) -> List[CaseResponse]:
        pass

    @abstractmethod
    async def get_case_by_id(self, case_id: UUID, user_id: UUID) -> CaseResponse | None:
        pass
