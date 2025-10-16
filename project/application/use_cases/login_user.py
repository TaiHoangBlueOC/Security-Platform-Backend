from project.application.dto.auth_dto import LoginResponse
from project.application.interfaces.user_repository_interface import \
    IUserRepository
from project.application.utils.hashing import verify_password
from project.application.utils.jwt_handler import create_access_token


class LoginUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        payload = {
            "sub": str(user.id),
            "username": user.username,
        }

        token = create_access_token(payload)
        return LoginResponse(access_token=token)
