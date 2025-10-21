from datetime import UTC, datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.application.interfaces.group_repository_interface import IGroupRepository
from project.domain.entities import GroupEntity
from project.infrastructure.database.models import (
    CaseModel,
    GroupModel,
    SharedCaseGroupModel,
    SharedCaseUserModel,
    UserGroupAssociationModel,
    UserModel,
)
from project.infrastructure.exceptions.exceptions import (
    AccessDeniedError,
    DuplicateAssociationError,
    NotFoundError,
)
from project.infrastructure.mappers.entity_mapper import EntityMapper


class GroupRepository(IGroupRepository):
    def __init__(self, session):
        self.session = session

    async def create_group(self, group_data: GroupEntity) -> GroupEntity:
        db_group = GroupModel(
            id=group_data.id,
            name=group_data.name,
            created_by=group_data.created_by,
        )

        self.session.add(db_group)
        await self.session.commit()
        await self.session.refresh(db_group)

        # Add creator as group member
        creator_association = UserGroupAssociationModel(
            user_id=group_data.created_by,
            group_id=group_data.id,
        )
        self.session.add(creator_association)
        await self.session.commit()

        group_data.created_at = db_group.created_at
        group_data.updated_at = db_group.updated_at
        return await self.get_group_by_id(group_data.id, group_data.created_by)

    # ------------------------------------------------------------
    # Get Groups for a User
    # ------------------------------------------------------------
    async def get_groups_by_user(self, user_id: UUID) -> List[GroupEntity]:
        stmt = (
            select(GroupModel)
            .join(UserGroupAssociationModel)
            .where(UserGroupAssociationModel.user_id == user_id)
            .options(selectinload(GroupModel.members).selectinload(UserModel.profile))
        )
        result = await self.session.execute(stmt)
        db_groups = result.scalars().unique().all()

        return [EntityMapper.to_group_entity(group) for group in db_groups]

    # ------------------------------------------------------------
    # Get Group by ID (only if user is a member)
    # ------------------------------------------------------------
    async def get_group_by_id(
        self, group_id: UUID, user_id: UUID
    ) -> Optional[GroupEntity]:
        stmt = (
            select(GroupModel)
            .join(UserGroupAssociationModel)
            .where(UserGroupAssociationModel.user_id == user_id)
            .where(GroupModel.id == group_id)
            .options(selectinload(GroupModel.members).selectinload(UserModel.profile))
        )
        result = await self.session.execute(stmt)
        db_group = result.scalars().first()

        if not db_group:
            raise AccessDeniedError("Group not found or access denied")

        return EntityMapper.to_group_entity(db_group)

    # ------------------------------------------------------------
    # Update Group (only if user is creator)
    # ------------------------------------------------------------
    async def update_group(self, group_data: GroupEntity) -> GroupEntity:
        stmt = select(GroupModel).where(
            GroupModel.id == group_data.id,
            GroupModel.created_by == group_data.created_by,
        )
        result = await self.session.execute(stmt)
        db_group = result.scalars().first()

        if not db_group:
            raise AccessDeniedError("Group not found or access denied")

        db_group.name = group_data.name
        db_group.updated_at = datetime.now(UTC)

        self.session.add(db_group)
        await self.session.commit()
        await self.session.refresh(db_group)

        return await self.get_group_by_id(group_data.id, group_data.created_by)

    # ------------------------------------------------------------
    # Delete Group (only if user is creator)
    # ------------------------------------------------------------
    async def delete_group(self, group_id: UUID, user_id: UUID) -> None:
        stmt = select(GroupModel).where(
            GroupModel.id == group_id,
            GroupModel.created_by == user_id,
        )
        result = await self.session.execute(stmt)
        db_group = result.scalars().first()

        if not db_group:
            raise AccessDeniedError("Group not found or access denied")

        await self.session.delete(db_group)
        await self.session.commit()

    # ------------------------------------------------------------
    # Add User to Group (only creator can add)
    # ------------------------------------------------------------
    async def add_user_to_group(
        self, user_to_add: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        # Verify group ownership
        stmt = select(GroupModel).where(
            GroupModel.id == group_id,
            GroupModel.created_by == user_id,
        )
        result = await self.session.execute(stmt)
        group = result.scalars().first()
        if not group:
            raise AccessDeniedError("Group not found or access denied")

        # Check if already in group
        stmt = select(UserGroupAssociationModel).where(
            UserGroupAssociationModel.user_id == user_to_add,
            UserGroupAssociationModel.group_id == group_id,
        )
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            raise DuplicateAssociationError("User already in group")

        association = UserGroupAssociationModel(
            user_id=user_to_add,
            group_id=group_id,
        )
        self.session.add(association)
        await self.session.commit()

    # ------------------------------------------------------------
    # Share Case with Group (check access)
    # ------------------------------------------------------------
    async def share_case_with_group(
        self, case_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        # Ensure user owns the case
        stmt = select(CaseModel).where(
            CaseModel.id == case_id,
            CaseModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        db_case = result.scalars().first()
        if not db_case:
            raise AccessDeniedError("Case not found or access denied")

        # Ensure group membership
        stmt = select(UserGroupAssociationModel).where(
            UserGroupAssociationModel.group_id == group_id
        )
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        if not members:
            raise NotFoundError("Group not found or empty")

        # Check if case already shared with group
        stmt = select(SharedCaseGroupModel).where(
            SharedCaseGroupModel.case_id == case_id,
            SharedCaseGroupModel.group_id == group_id,
        )
        result = await self.session.execute(stmt)
        shared = result.scalars().first()
        if shared:
            raise DuplicateAssociationError("Case already shared with this group")

        # Share with group
        shared_group = SharedCaseGroupModel(case_id=case_id, group_id=group_id)
        self.session.add(shared_group)

        # Also share with each member (via SharedCaseUserModel)
        for member in members:
            self.session.add(
                SharedCaseUserModel(case_id=case_id, user_id=member.user_id)
            )

        await self.session.commit()

    # ------------------------------------------------------------
    # Remove User from Group (only creator can remove)
    # ------------------------------------------------------------
    async def remove_user_from_group(
        self, user_to_remove_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        # Verify group ownership
        stmt = select(GroupModel).where(
            GroupModel.id == group_id,
            GroupModel.created_by == user_id,
        )
        result = await self.session.execute(stmt)
        group = result.scalars().first()
        if not group:
            raise AccessDeniedError("Group not found or access denied")

        # Find association
        stmt = select(UserGroupAssociationModel).where(
            UserGroupAssociationModel.user_id == user_to_remove_id,
            UserGroupAssociationModel.group_id == group_id,
        )
        result = await self.session.execute(stmt)
        association = result.scalars().first()
        if not association:
            raise NotFoundError("User not in group")

        await self.session.delete(association)
        await self.session.commit()

    # ------------------------------------------------------------
    # Remove Case from Group (only creator can remove)
    # ------------------------------------------------------------
    async def remove_case_from_group(
        self, case_id: UUID, group_id: UUID, user_id: UUID
    ) -> None:
        # Verify group ownership
        stmt = select(GroupModel).where(
            GroupModel.id == group_id,
            GroupModel.created_by == user_id,
        )
        result = await self.session.execute(stmt)
        group = result.scalars().first()
        if not group:
            raise AccessDeniedError("Group not found or access denied")

        # Find shared case association
        stmt = select(SharedCaseGroupModel).where(
            SharedCaseGroupModel.case_id == case_id,
            SharedCaseGroupModel.group_id == group_id,
        )
        result = await self.session.execute(stmt)
        shared = result.scalars().first()
        if not shared:
            raise NotFoundError("Case not shared with group")

        await self.session.delete(shared)
        await self.session.commit()
