from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from project.application.dto.group_management_dto import (
    CreateGroupRequest,
    GroupResponse,
    UpdateGroupRequest,
)
from project.application.interfaces.group_repository_interface import IGroupRepository
from project.application.use_cases.group_management.group_management_use_case import (
    GroupManagementUseCase,
)
from project.dependencies.repository_dependency import get_group_repo
from project.presentation.dependencies.authentication_dependency import get_user_info

router = APIRouter(tags=["Group Management"], prefix="/groups")


# ----------------------------
# GROUP CRUD
# ----------------------------
@router.get("", response_model=List[GroupResponse])
async def get_groups_by_user(
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    return await use_group.get_groups_by_user(user.id)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group_by_id(
    group_id: UUID,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    group = await use_group.get_group(group_id, user.id)
    return group


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    data: CreateGroupRequest,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    return await use_group.create_group(data, user.id)


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: UUID,
    data: UpdateGroupRequest,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    return await use_group.update_group(group_id, user.id, data)


@router.delete("/{group_id}")
async def delete_group(
    group_id: UUID,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    await use_group.delete_group(group_id, user.id)
    return {"message": f"Group {group_id} deleted successfully"}


@router.post(
    "/{group_id}/users/{user_to_add_id}",
)
async def add_user_to_group(
    group_id: UUID,
    user_to_add_id: UUID,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    await use_group.add_user_to_group(
        user_to_add_id=user_to_add_id, group_id=group_id, user_id=user.id
    )

    return {"message": f"User {user_to_add_id} added to group {group_id} successfully"}


@router.post(
    "/{group_id}/cases/{case_id}",
)
async def share_case_with_group(
    group_id: UUID,
    case_id: UUID,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    await use_group.share_case_with_group(case_id, group_id, user.id)

    return {"message": f"Case {case_id} shared with group {group_id} successfully"}


@router.delete(
    "/{group_id}/users/{user_to_remove_id}",
)
async def remove_user_from_group(
    group_id: UUID,
    user_to_remove_id: UUID,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    await use_group.remove_user_from_group(
        user_to_remove_id=user_to_remove_id, group_id=group_id, user_id=user.id
    )
    return {
        "message": f"User {user_to_remove_id} removed from group {group_id} successfully"
    }


@router.delete(
    "/{group_id}/cases/{case_id}",
)
async def remove_case_from_group(
    group_id: UUID,
    case_id: UUID,
    repo: IGroupRepository = Depends(get_group_repo),
    user=Depends(get_user_info),
):
    use_group = GroupManagementUseCase(repo)
    await use_group.remove_case_from_group(
        case_id=case_id, group_id=group_id, user_id=user.id
    )
    return {"message": f"Case {case_id} removed from group {group_id} successfully"}
