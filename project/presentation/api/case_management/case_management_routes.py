from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from project.application.dto.case_management_dto import (
    CaseResponse,
    CollectionResponse,
    CreateCaseCollectionRequest,
    CreateCaseRequest,
    UpdateCaseCollectionRequest,
    UpdateCaseRequest,
)
from project.application.interfaces.case_repository_interface import ICaseRepository
from project.application.use_cases.case_management.case_management_use_case import (
    CaseManagementUseCase,
)
from project.dependencies.repository_dependency import get_case_repo
from project.presentation.dependencies.authentication_dependency import get_user_info

router = APIRouter(tags=["Case Management"])


# ----------------------------
# CASE CRUD
# ----------------------------
@router.get("/cases", response_model=List[CaseResponse])
async def get_cases_by_user(
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        return await use_case.get_cases_by_user(user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case_by_id(
    case_id: UUID,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    case = await use_case.get_case(case_id, user.id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )
    return case


@router.post("/cases", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    data: CreateCaseRequest,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        return await use_case.create_case(data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/cases/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: UUID,
    data: UpdateCaseRequest,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        return await use_case.update_case(case_id, user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/cases/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: UUID,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        await use_case.delete_case(case_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ----------------------------
# CASE COLLECTION CRUD
# ----------------------------
@router.get("/collections", response_model=List[CollectionResponse])
async def get_collections_by_user(
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)

    return await use_case.get_collections_by_user(user.id)


@router.get("/collections/{collection_id}", response_model=CollectionResponse)
async def get_collection_by_id(
    collection_id: UUID,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)

    return await use_case.get_collection(collection_id, user.id)


@router.post(
    "/collections",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_collection(
    data: CreateCaseCollectionRequest,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        return await use_case.create_collection(data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/collections/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_id: UUID,
    data: UpdateCaseCollectionRequest,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        return await use_case.update_collection(collection_id, user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/collections/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: UUID,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        await use_case.delete_collection(collection_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/collections/{collection_id}/cases/{case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_case_to_collection(
    collection_id: UUID,
    case_id: UUID,
    repo: ICaseRepository = Depends(get_case_repo),
    user=Depends(get_user_info),
):
    use_case = CaseManagementUseCase(repo)
    try:
        await use_case.add_case_to_collection(collection_id, case_id, user.id)
        return "Created"
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
