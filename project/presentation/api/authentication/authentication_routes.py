from fastapi import APIRouter, Depends, HTTPException, status

from project.application.dto.auth_dto import (LoginRequest, LoginResponse,
                                              RegisterRequest, UserResponse)
from project.application.interfaces.user_repository_interface import \
    IUserRepository
from project.application.use_cases.login_user import LoginUserUseCase
from project.application.use_cases.register_user import RegisterUserUseCase
from project.dependencies.repository_dependency import get_user_repo
from project.presentation.dependencies.authentication_dependency import \
    get_user_info

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user(
    data: RegisterRequest, repo: IUserRepository = Depends(get_user_repo())
) -> UserResponse:
    use_case = RegisterUserUseCase(repo)

    try:
        return await use_case.execute(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login_user(
    data: LoginRequest, repo: IUserRepository = Depends(get_user_repo())
):
    login_use_case = LoginUserUseCase(repo)

    try:
        return await login_use_case.execute(data.username, data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user: UserResponse = Depends(get_user_info)):
    """Return current logged-in user's info."""
    return current_user
