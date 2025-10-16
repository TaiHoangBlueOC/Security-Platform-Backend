from fastapi import APIRouter, Depends, HTTPException, status

from project.application.dto.processing_file_dto import (CreateCaseRequest,
                                                         CreateCaseResponse)
from project.application.use_cases.create_case import CreateCaseUseCase
from project.infrastructure.database.session import get_async_db
from project.infrastructure.repositories.case_repository import CaseRepository
from project.presentation.dependencies.authentication_dependency import \
    get_user_info

router = APIRouter(prefix="/cases", tags=["Case Management"])


@router.post("/")
async def create_case(
    data: CreateCaseRequest, db=Depends(get_async_db), user=Depends(get_user_info)
) -> CreateCaseResponse:
    repo = CaseRepository(db)
    use_case = CreateCaseUseCase(repo)

    try:
        case = await use_case.execute(data.title, data.description, data.slug, user)
        return CreateCaseResponse(
            id=case.id,
            title=case.title,
            description=case.description,
            slug=case.slug,
            status=case.status,
            created_at=case.created_at,
            updated_at=case.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
