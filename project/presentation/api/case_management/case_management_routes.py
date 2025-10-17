from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from project.application.dto.processing_file_dto import (CaseResponse,
                                                         CreateCaseRequest)
from project.application.interfaces.case_repository_interface import \
    ICaseRepository
from project.application.use_cases.case_management.create_case import \
    CreateCaseUseCase
from project.application.use_cases.case_management.get_case import (
    GetCasesByUserUseCase, GetCaseUseCase)
from project.dependencies.repository_dependency import get_case_repo
from project.presentation.dependencies.authentication_dependency import \
    get_user_info

router = APIRouter(prefix="/cases", tags=["Case Management"])


@router.get("/{case_id}")
async def get_case_by_id(
    case_id: str,
    repo: ICaseRepository = Depends(get_case_repo()),
    user=Depends(get_user_info),
) -> CaseResponse:
    use_case = GetCaseUseCase(repo)

    try:
        case = await use_case.execute(case_id, user.id)
        if case is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Case not found"
            )
        return case
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/")
async def get_cases_by_user(
    repo: ICaseRepository = Depends(get_case_repo()),
    user=Depends(get_user_info),
) -> List[CaseResponse]:
    use_case = GetCasesByUserUseCase(repo)

    try:
        return await use_case.execute(user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/")
async def create_case(
    data: CreateCaseRequest,
    repo: ICaseRepository = Depends(get_case_repo()),
    user=Depends(get_user_info),
) -> CaseResponse:
    use_case = CreateCaseUseCase(repo)

    try:
        return await use_case.execute(data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
