import uuid

from project.application.dto.auth_dto import RegisterRequest
from project.application.interfaces.user_repository_interface import \
    IUserRepository
from project.application.utils.hashing import hash_password
from project.domain.entities import ProfileEntity, UserEntity
from project.domain.enums import UserRole


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_info: RegisterRequest):
        # Check if user exists
        existing_user = await self.user_repo.get_by_username(user_info.username)
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = hash_password(user_info.password)

        user_id = uuid.uuid4()

        user_entity = UserEntity(
            id=user_id,
            username=user_info.username,
            role=UserRole.USER,
            hashed_password=hashed_password,
        )

        profile = ProfileEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
        )

        return await self.user_repo.create_user(user_entity, profile)
