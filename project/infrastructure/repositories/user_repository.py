from sqlalchemy import select

from project.application.interfaces.user_repository_interface import IUserRepository
from project.domain.entities import UserEntity
from project.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_username(self, username: str):
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        return UserEntity(
            id=user.id,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def create_user(self, user: UserEntity):
        db_user = UserModel(
            username=user.username,
            hashed_password=user.hashed_password,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        user.id = db_user.id
        return user
