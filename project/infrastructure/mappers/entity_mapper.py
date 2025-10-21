from project.domain.entities import GroupEntity, ProfileEntity, UserEntity


class EntityMapper:
    @staticmethod
    def to_profile_entity(profile_model) -> ProfileEntity:
        return ProfileEntity(
            id=profile_model.id,
            user_id=profile_model.user_id,
            first_name=profile_model.first_name,
            last_name=profile_model.last_name,
            created_at=profile_model.created_at,
            updated_at=profile_model.updated_at,
        )

    @staticmethod
    def to_user_entity(user_model) -> UserEntity:
        return UserEntity(
            id=user_model.id,
            username=user_model.username,
            profile=EntityMapper.to_profile_entity(user_model.profile),
            role=user_model.role,
            hashed_password=None,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    @staticmethod
    def to_group_entity(group_model) -> GroupEntity:
        return GroupEntity(
            id=group_model.id,
            name=group_model.name,
            created_by=group_model.created_by,
            members=[
                EntityMapper.to_user_entity(member) for member in group_model.members
            ],
            created_at=group_model.created_at,
            updated_at=group_model.updated_at,
        )
