from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from project.application.dto.auth_dto import UserResponse
from project.application.interfaces.user_repository_interface import \
    IUserRepository
from project.application.use_cases.get_user_info import GetUserInfoUseCase
from project.dependencies.repository_dependency import get_user_repo

bearer_schema = HTTPBearer()


async def get_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
    repo: IUserRepository = Depends(get_user_repo()),
) -> UserResponse:
    """
    Extract JWT token from Authorization header and return the current logged-in user.
    """
    token = credentials.credentials
    use_case = GetUserInfoUseCase(repo)

    try:
        user = await use_case.execute(token)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
