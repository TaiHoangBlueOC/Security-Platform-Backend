from abc import ABC, abstractmethod

from project.domain.entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        pass
