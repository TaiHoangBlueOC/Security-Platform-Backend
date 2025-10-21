from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from project.application.interfaces.case_repository_interface import ICaseRepository
from project.domain.entities import CaseEntity, CollectionEntity
from project.infrastructure.database.models import (
    CaseCollectionAssociationModel,
    CaseModel,
    CollectionModel,
    SharedCaseUserModel,
)
from project.infrastructure.exceptions.exceptions import (
    AccessDeniedError,
    DuplicateAssociationError,
    NotFoundError,
)


class CaseRepository(ICaseRepository):

    def __init__(self, session):
        self.session = session

    async def create_case(self, case: CaseEntity) -> CaseEntity:
        db_case = CaseModel(
            id=case.id,
            user_id=case.user_id,
            title=case.title,
            status=case.status,
            description=case.description,
            slug=case.slug,
        )

        self.session.add(db_case)
        await self.session.commit()
        await self.session.refresh(db_case)

        # Create view permission for the case owner
        shared_relationships = SharedCaseUserModel(
            case_id=case.id, user_id=case.user_id
        )
        self.session.add(shared_relationships)
        await self.session.commit()

        case.created_at = db_case.created_at

        return case

    async def get_case_by_id(
        self, case_id: UUID, user_id: UUID
    ) -> Optional[CaseEntity]:
        # Check if user has access to the case
        stmt = (
            select(SharedCaseUserModel)
            .where(SharedCaseUserModel.user_id == user_id)
            .where(SharedCaseUserModel.case_id == case_id)
        )
        result = await self.session.execute(stmt)
        shared_case = result.scalars().first()
        if not shared_case:
            raise AccessDeniedError("Case not found or access denied")

        # Fetch the case
        stmt = (
            select(CaseModel)
            .where(CaseModel.id == case_id)
            .options(joinedload(CaseModel.evidences))
        )
        result = await self.session.execute(stmt)
        db_case = result.scalars().first()
        if not db_case:
            raise NotFoundError("Case not found")

        return CaseEntity(
            id=db_case.id,
            user_id=db_case.user_id,
            title=db_case.title,
            status=db_case.status,
            description=db_case.description,
            slug=db_case.slug,
            summary=db_case.summary,
            created_at=db_case.created_at,
            updated_at=db_case.updated_at,
        )

    async def get_cases_by_user(self, user_id: UUID) -> List[CaseEntity]:
        stmt = (
            select(CaseModel)
            .where(CaseModel.user_id == user_id)
            .options(joinedload(CaseModel.evidences))
        )
        result = await self.session.execute(stmt)
        cases = result.unique().scalars().all()
        return [
            CaseEntity(
                id=db_case.id,
                user_id=db_case.user_id,
                title=db_case.title,
                status=db_case.status,
                description=db_case.description,
                slug=db_case.slug,
                summary=db_case.summary,
                created_at=db_case.created_at,
                updated_at=db_case.updated_at,
            )
            for db_case in cases
        ]

    async def create_collection(self, collection: CollectionEntity) -> CollectionEntity:
        db_collection = CollectionModel(
            id=collection.id,
            user_id=collection.user_id,
            title=collection.title,
            description=collection.description,
        )

        self.session.add(db_collection)
        await self.session.commit()
        await self.session.refresh(db_collection)

        return db_collection

    async def update_case(self, case_data: CaseEntity) -> CaseEntity:
        # Fetch existing case
        stmt = select(CaseModel).where(
            CaseModel.id == case_data.id,
            CaseModel.user_id == case_data.user_id,
        )
        result = await self.session.execute(stmt)
        db_case = result.scalars().first()
        if not db_case:
            raise AccessDeniedError("Case not found or access denied")

        # Update only fields that changed
        db_case.title = case_data.title
        db_case.description = case_data.description
        db_case.slug = case_data.slug
        db_case.summary = case_data.summary
        db_case.status = case_data.status

        await self.session.commit()
        await self.session.refresh(db_case)

        return CaseEntity(
            id=db_case.id,
            user_id=db_case.user_id,
            title=db_case.title,
            status=db_case.status,
            description=db_case.description,
            slug=db_case.slug,
            summary=db_case.summary,
            created_at=db_case.created_at,
            updated_at=db_case.updated_at,
        )

    async def delete_case(self, case_id: UUID, user_id: UUID) -> None:
        stmt = select(CaseModel).where(
            CaseModel.id == case_id, CaseModel.user_id == user_id
        )
        result = await self.session.execute(stmt)
        db_case = result.scalars().first()
        if not db_case:
            raise AccessDeniedError("Case not found or access denied")

        await self.session.delete(db_case)
        await self.session.commit()

    async def get_collections_by_user(self, user_id: UUID) -> List[CollectionEntity]:
        stmt = (
            select(CollectionModel)
            .where(CollectionModel.user_id == user_id)
            .options(selectinload(CollectionModel.cases))
        )
        result = await self.session.execute(stmt)
        collections = result.scalars().all()

        # Map to entities with detailed case info
        return [
            CollectionEntity(
                id=collection.id,
                user_id=collection.user_id,
                title=collection.title,
                description=collection.description,
                created_at=collection.created_at,
                updated_at=collection.updated_at,
                cases=[
                    CaseEntity(
                        id=case.id,
                        user_id=case.user_id,
                        title=case.title,
                        status=case.status,
                        description=case.description,
                        slug=case.slug,
                        summary=case.summary,
                        created_at=case.created_at,
                        updated_at=case.updated_at,
                    )
                    for case in collection.cases
                ],
            )
            for collection in collections
        ]

    async def get_collection_by_id(
        self, collection_id: UUID, user_id: UUID
    ) -> Optional[CollectionEntity]:
        stmt = (
            select(CollectionModel)
            .options(selectinload(CollectionModel.cases))
            .where(
                CollectionModel.id == collection_id,
                CollectionModel.user_id == user_id,
            )
        )
        result = await self.session.execute(stmt)
        collection = result.scalars().first()

        if not collection:
            raise AccessDeniedError("Collection not found or access denied")

        # Map to entity
        return CollectionEntity(
            id=collection.id,
            user_id=collection.user_id,
            title=collection.title,
            description=collection.description,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            cases=[
                CaseEntity(
                    id=case.id,
                    user_id=case.user_id,
                    title=case.title,
                    status=case.status,
                    description=case.description,
                    slug=case.slug,
                    summary=case.summary,
                    created_at=case.created_at,
                    updated_at=case.updated_at,
                )
                for case in collection.cases
            ],
        )

    async def update_collection(
        self, collection_id: UUID, user_id: UUID, collection_data: CollectionEntity
    ) -> CollectionEntity:
        stmt = select(CollectionModel).where(
            CollectionModel.id == collection_id,
            CollectionModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        db_collection = result.scalars().first()
        if not db_collection:
            raise AccessDeniedError("Collection not found or access denied")

        db_collection.title = collection_data.title
        db_collection.description = collection_data.description

        self.session.add(db_collection)
        await self.session.commit()
        await self.session.refresh(db_collection)

        return CollectionEntity(
            id=db_collection.id,
            user_id=db_collection.user_id,
            title=db_collection.title,
            description=db_collection.description,
            created_at=db_collection.created_at,
            updated_at=db_collection.updated_at,
        )

    async def delete_collection(self, collection_id: UUID, user_id: UUID) -> None:
        stmt = select(CollectionModel).where(
            CollectionModel.id == collection_id,
            CollectionModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        db_collection = result.scalars().first()
        if not db_collection:
            raise AccessDeniedError("Collection not found or access denied")

        await self.session.delete(db_collection)
        await self.session.commit()

    async def add_case_to_collection(
        self, collection_id: UUID, case_id: UUID, user_id: UUID
    ) -> None:
        # Check if the collection belongs to the user
        stmt = select(CollectionModel).where(
            CollectionModel.id == collection_id,
            CollectionModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        collection = result.scalars().first()
        if not collection:
            raise AccessDeniedError("Collection not found or access denied")

        # Check if the case exists and belongs to the user
        stmt = select(CaseModel).where(
            CaseModel.id == case_id,
            CaseModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        case = result.scalars().first()
        if not case:
            raise AccessDeniedError("Case not found or access denied")

        # Check if association already exists
        stmt = select(CaseCollectionAssociationModel).where(
            CaseCollectionAssociationModel.collection_id == collection_id,
            CaseCollectionAssociationModel.case_id == case_id,
        )
        result = await self.session.execute(stmt)
        association = result.scalars().first()
        if association:
            raise DuplicateAssociationError("Case is already part of the collection")

        # Create association
        association = CaseCollectionAssociationModel(
            collection_id=collection_id,
            case_id=case_id,
        )
        self.session.add(association)
        await self.session.commit()
