import uuid
from datetime import UTC, datetime

from project.application.interfaces.user_repository_interface import IUserRepository
from project.domain.entities import UserEntity
from project.infrastructure.security.hashing import hash_password


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str):
        # Check if user exists
        existing_user = await self.user_repo.get_by_username(username)
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = hash_password(password)
        user_entity = UserEntity(
            id=uuid.uuid4(),
            username=username,
            hashed_password=hashed_password,
            created_at=datetime.now(UTC),
        )

        return await self.user_repo.create_user(user_entity)
