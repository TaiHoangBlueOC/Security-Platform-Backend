import uuid

from project.application.dto.auth_dto import LoginResponse, RegisterRequest
from project.application.exceptions.exceptions import (
    AuthenticationException,
    ResourceConflictException,
    ResourceNotFoundException,
)
from project.application.interfaces.user_repository_interface import IUserRepository
from project.application.utils.hashing import hash_password, verify_password
from project.application.utils.jwt_handler import (
    create_access_token,
    decode_access_token,
)
from project.domain.entities import ProfileEntity, UserEntity
from project.domain.enums import UserRole


class AuthenticationUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def login(self, username: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_username(username)

        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationException("Invalid username or password")

        payload = {
            "sub": str(user.id),
            "username": user.username,
        }

        token = create_access_token(payload)
        return LoginResponse(access_token=token)

    async def register(self, user_info: RegisterRequest):
        # Check if user exists
        existing_user = await self.user_repo.get_by_username(user_info.username)

        if existing_user:
            raise ResourceConflictException(
                f"Username {user_info.username} is already taken"
            )

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

    async def get_info(self, token: str) -> UserEntity:
        payload = decode_access_token(token)

        user = await self.user_repo.get_by_username(payload["username"])
        if user is None:
            raise ResourceNotFoundException("User not found")

        return user
