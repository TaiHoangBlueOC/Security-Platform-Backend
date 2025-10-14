from project.application.interfaces.user_repository_interface import IUserRepository
from project.infrastructure.security.hashing import verify_password
from project.infrastructure.security.jwt_handler import create_access_token
from project.presentation.dto.auth_dto import LoginResponse


class LoginUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        token = create_access_token({"sub": user.username})
        return LoginResponse(access_token=token)
