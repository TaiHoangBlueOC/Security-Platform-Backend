from fastapi import APIRouter, Depends, HTTPException, status

from project.application.use_cases.login_user import LoginUserUseCase
from project.application.use_cases.register_user import RegisterUserUseCase
from project.domain.entities import UserEntity
from project.infrastructure.database.session import get_db
from project.infrastructure.repositories.user_repository import UserRepository
from project.presentation.dependencies.authentication_dependency import get_user_info
from project.presentation.dto.auth_dto import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user(data: RegisterRequest, db=Depends(get_db)) -> RegisterResponse:
    repo = UserRepository(db)
    use_case = RegisterUserUseCase(repo)

    try:
        user = await use_case.execute(data.username, data.password)
        return RegisterResponse(
            id=user.id, username=user.username, created_at=user.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login_user(data: LoginRequest, db=Depends(get_db)):
    repo = UserRepository(db)
    login_use_case = LoginUserUseCase(repo)

    try:
        return await login_use_case.execute(data.username, data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user: UserEntity = Depends(get_user_info)):
    """Return current logged-in user's info."""
    return current_user
