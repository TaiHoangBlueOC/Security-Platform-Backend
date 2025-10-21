from project.application.dto.group_management_dto import (
    CaseResponse,
    GroupResponse,
    UserResponse,
)
from project.domain.entities import GroupEntity, UserEntity


class DtoMapper:
    @staticmethod
    def to_user_response(user_entity: UserEntity) -> UserResponse:
        return UserResponse(
            id=user_entity.id,
            username=user_entity.username,
            first_name=user_entity.profile.first_name if user_entity.profile else None,
            last_name=user_entity.profile.last_name if user_entity.profile else None,
            created_at=user_entity.created_at,
        )

    @staticmethod
    def to_group_response(group_entity: GroupEntity) -> GroupResponse:
        return GroupResponse(
            id=group_entity.id,
            name=group_entity.name,
            created_by=group_entity.created_by,
            members=[
                DtoMapper.to_user_response(member) for member in group_entity.members
            ],
            cases=[
                CaseResponse(
                    id=case.id,
                    user_id=case.user_id,
                    title=case.title,
                    status=case.status,
                    created_at=case.created_at,
                )
                for case in group_entity.cases
            ],
            created_at=group_entity.created_at,
            updated_at=group_entity.updated_at,
        )
