import uuid
from typing import List
from uuid import UUID

from project.application.dto.group_management_dto import (
    CreateGroupRequest,
    GroupResponse,
    UpdateGroupRequest,
)
from project.application.exceptions.exceptions import (
    UnauthorizedAccessException,
    handle_repo_exceptions,
)
from project.application.interfaces.group_repository_interface import IGroupRepository
from project.application.mappers.dto_mapper import DtoMapper
from project.domain.entities import GroupEntity


class GroupManagementUseCase:
    def __init__(self, group_repo: IGroupRepository):
        self.group_repo = group_repo

    # ----------------------------
    # GROUP CRUD
    # ----------------------------
    @handle_repo_exceptions
    async def create_group(
        self, group_request: CreateGroupRequest, user_id: uuid.UUID
    ) -> GroupResponse:
        """Create a new group owned by the user."""

        group_entity = GroupEntity(
            id=uuid.uuid4(),
            name=group_request.name,
            created_by=user_id,
        )

        group = await self.group_repo.create_group(group_entity)

        return DtoMapper.to_group_response(group)

    @handle_repo_exceptions
    async def get_group(self, group_id: UUID, user_id: UUID) -> GroupResponse:
        """Retrieve a group by ID (only if the user is a member or owner)."""
        group = await self.group_repo.get_group_by_id(group_id, user_id)

        return DtoMapper.to_group_response(group)

    @handle_repo_exceptions
    async def get_groups_by_user(self, user_id: UUID) -> List[GroupResponse]:
        """Retrieve all groups the user owns or belongs to."""
        groups = await self.group_repo.get_groups_by_user(user_id)

        return [DtoMapper.to_group_response(group) for group in groups]

    @handle_repo_exceptions
    async def update_group(
        self, group_id: UUID, user_id: UUID, group_request: UpdateGroupRequest
    ) -> GroupResponse:
        """Update an existing group (only by the owner)."""
        existing_group = await self.group_repo.get_group_by_id(group_id, user_id)

        if existing_group.created_by != user_id:
            raise UnauthorizedAccessException(
                "Only the group owner can update the group."
            )

        updated_group = GroupEntity(
            id=group_id,
            name=group_request.name or existing_group.name,
            created_by=existing_group.created_by,
            members=existing_group.members,
            created_at=existing_group.created_at,
        )

        group = await self.group_repo.update_group(updated_group)

        return DtoMapper.to_group_response(group)

    @handle_repo_exceptions
    async def delete_group(self, group_id: UUID, user_id: UUID) -> None:
        """Delete a group (only by the owner)."""
        await self.group_repo.delete_group(group_id, user_id)

    # ----------------------------
    # GROUP MEMBERS
    # ----------------------------
    @handle_repo_exceptions
    async def add_user_to_group(
        self, group_id: UUID, user_to_add_id: UUID, user_id: UUID
    ) -> None:
        """Add a user to a group (only if the current user is the owner)."""

        await self.group_repo.add_user_to_group(user_to_add_id, group_id, user_id)

    @handle_repo_exceptions
    async def remove_user_from_group(
        self, user_to_remove_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        """Remove a user from a group (only if the current user is the owner)."""
        if user_to_remove_id == user_id:
            raise UnauthorizedAccessException(
                "Group owners cannot remove themselves from the group."
            )

        await self.group_repo.remove_user_from_group(
            user_to_remove_id, group_id, user_id
        )

    # ----------------------------
    # CASE SHARING
    # ----------------------------
    @handle_repo_exceptions
    async def share_case_with_group(
        self, case_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        """Share a case with a group."""

        await self.group_repo.share_case_with_group(case_id, group_id, user_id)

    @handle_repo_exceptions
    async def remove_case_from_group(
        self, case_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        """Remove a case from a group (only if the current user is the owner)."""
        await self.group_repo.remove_case_from_group(case_id, group_id, user_id)
