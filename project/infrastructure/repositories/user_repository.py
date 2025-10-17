from sqlalchemy import select
from sqlalchemy.orm import joinedload

from project.application.dto.auth_dto import UserInternal
from project.application.interfaces.user_repository_interface import \
    IUserRepository
from project.domain.entities import ProfileEntity, UserEntity
from project.infrastructure.database.models import ProfileModel, UserModel


class UserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_username(self, username: str):
        stmt = (
            select(UserModel)
            .where(UserModel.username == username)
            .options(joinedload(UserModel.profile))
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        return UserInternal(
            id=user.id,
            username=user.username,
            first_name=user.profile.first_name if user.profile else None,
            last_name=user.profile.last_name if user.profile else None,
            role=user.role,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def create_user(self, user: UserEntity, profile: ProfileEntity):
        db_user = UserModel(
            username=user.username,
            hashed_password=user.hashed_password,
            role=user.role,
        )

        db_profile = ProfileModel(
            user_id=user.id, first_name=profile.first_name, last_name=profile.last_name
        )

        db_user.profile = db_profile

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return UserInternal(
            id=db_user.id,
            username=db_user.username,
            first_name=db_profile.first_name,
            last_name=db_profile.last_name,
            role=db_user.role,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )
