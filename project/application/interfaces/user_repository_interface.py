from abc import ABC, abstractmethod
from typing import Optional

from project.application.dto.auth_dto import UserInternal
from project.domain.entities import ProfileEntity, UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(
        self, user: UserEntity, profile: ProfileEntity
    ) -> UserInternal:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserInternal]:
        pass
