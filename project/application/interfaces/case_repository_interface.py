from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from project.domain.entities import CaseEntity, CollectionEntity


class ICaseRepository(ABC):
    @abstractmethod
    async def create_case(self, case_data: CaseEntity) -> CaseEntity:
        pass

    @abstractmethod
    async def get_cases_by_user(self, user_id: UUID) -> List[CaseEntity]:
        pass

    @abstractmethod
    async def get_case_by_id(
        self, case_id: UUID, user_id: UUID
    ) -> Optional[CaseEntity]:
        pass

    @abstractmethod
    async def update_case(self, case_data: CaseEntity) -> CaseEntity:
        pass

    @abstractmethod
    async def delete_case(self, case_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def create_collection(self, collection: CollectionEntity) -> CollectionEntity:
        pass

    @abstractmethod
    async def get_collections_by_user(self, user_id: UUID) -> List[CollectionEntity]:
        pass

    @abstractmethod
    async def get_collection_by_id(
        self, collection_id: UUID, user_id: UUID
    ) -> Optional[CollectionEntity]:
        pass

    @abstractmethod
    async def update_collection(
        self, collection_id: UUID, user_id: UUID, collection_data: CollectionEntity
    ) -> CollectionEntity:
        pass

    @abstractmethod
    async def delete_collection(self, collection_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def add_case_to_collection(
        self, collection_id: UUID, case_id: UUID, user_id: UUID
    ) -> None:
        pass
