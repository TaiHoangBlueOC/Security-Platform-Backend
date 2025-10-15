from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from project.application.use_cases.get_user_info import GetUserInfoUseCase
from project.domain.entities import UserEntity
from project.infrastructure.database.session import get_db
from project.infrastructure.repositories.user_repository import UserRepository

bearer_schema = HTTPBearer()


async def get_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
    db=Depends(get_db),
) -> UserEntity:
    """
    Extract JWT token from Authorization header and return the current logged-in user.
    """
    token = credentials.credentials
    repo = UserRepository(db)
    use_case = GetUserInfoUseCase(repo)

    try:
        user = await use_case.execute(token)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
