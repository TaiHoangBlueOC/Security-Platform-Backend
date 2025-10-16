from project.application.utils.jwt_handler import decode_access_token
from project.domain.entities import UserEntity
from project.infrastructure.repositories.user_repository import IUserRepository


class GetUserInfoUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, token: str) -> UserEntity:
        payload = decode_access_token(token)

        user = await self.user_repo.get_by_username(payload["username"])
        if user is None:
            raise ValueError("User not found")

        return user
