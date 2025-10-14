from jose import JWTError, jwt

from project.domain.entities import UserEntity
from project.infrastructure.repositories.user_repository import IUserRepository
from runtime_settings import JWT_ALGORITHM, JWT_SECRET_KEY


class GetUserInfoUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, token: str) -> UserEntity:
        """Decode JWT and return the associated user."""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise ValueError("Invalid token: missing email claim")
        except JWTError:
            raise ValueError("Invalid or expired token")

        user = await self.user_repo.get_by_username(username)
        if user is None:
            raise ValueError("User not found")

        return user
