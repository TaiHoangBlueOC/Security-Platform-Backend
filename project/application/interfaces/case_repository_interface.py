from abc import ABC, abstractmethod
from typing import List

from project.domain.entities import CaseEntity


class ICaseRepository(ABC):
    @abstractmethod
    async def create_case(self, case: CaseEntity) -> CaseEntity:
        pass

    @abstractmethod
    async def get_cases_by_user(self, user_id: str) -> List[CaseEntity]:
        pass
