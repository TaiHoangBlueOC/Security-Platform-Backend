from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from project.domain.entities import GroupEntity


class IGroupRepository(ABC):
    @abstractmethod
    async def create_group(self, group_data: GroupEntity) -> GroupEntity:
        pass

    @abstractmethod
    async def get_groups_by_user(self, user_id: UUID) -> List[GroupEntity]:
        pass

    @abstractmethod
    async def get_group_by_id(
        self, group_id: UUID, user_id: UUID
    ) -> Optional[GroupEntity]:
        pass

    @abstractmethod
    async def update_group(self, group_data: GroupEntity) -> GroupEntity:
        pass

    @abstractmethod
    async def delete_group(self, group_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def add_user_to_group(
        self, user_to_add, group_id: UUID, user_id: UUID
    ) -> None:
        pass

    @abstractmethod
    async def share_case_with_group(
        self, case_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        pass

    @abstractmethod
    async def remove_user_from_group(
        self, user_to_remove_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        pass

    @abstractmethod
    async def remove_case_from_group(
        self, case_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        pass
