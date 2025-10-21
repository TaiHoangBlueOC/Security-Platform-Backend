import uuid
from typing import List
from uuid import UUID

from project.application.dto.case_management_dto import (
    CaseResponse,
    CollectionResponse,
    CreateCaseCollectionRequest,
    CreateCaseRequest,
    UpdateCaseCollectionRequest,
    UpdateCaseRequest,
)
from project.application.exceptions.exceptions import handle_repo_exceptions
from project.application.interfaces.case_repository_interface import ICaseRepository
from project.domain.entities import CaseEntity, CollectionEntity
from project.domain.enums import CaseStatus


class CaseManagementUseCase:
    def __init__(self, case_repo: ICaseRepository):
        self.case_repo = case_repo

    # ----------------------------
    # CASES
    # ----------------------------
    @handle_repo_exceptions
    async def create_case(
        self, case_request: CreateCaseRequest, user_id: uuid.UUID
    ) -> CaseResponse:

        case_entity = CaseEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            title=case_request.title,
            status=CaseStatus.OPEN,
            description=case_request.description,
            slug=case_request.slug,
        )

        case = await self.case_repo.create_case(case_entity)

        return CaseResponse(
            id=case.id,
            user_id=case.user_id,
            title=case.title,
            description=case.description,
            slug=case.slug,
            status=case.status.value,
            summary=case.summary,
            evidences=[],
            created_at=case.created_at,
            updated_at=case.updated_at,
        )

    @handle_repo_exceptions
    async def get_case(self, case_id: UUID, user_id: UUID) -> CaseResponse:
        case = await self.case_repo.get_case_by_id(case_id, user_id)

        return CaseResponse(
            id=case.id,
            user_id=case.user_id,
            title=case.title,
            description=case.description,
            slug=case.slug,
            status=case.status,
            summary=case.summary,
            evidences=[],
            created_at=case.created_at,
            updated_at=case.updated_at,
        )

    @handle_repo_exceptions
    async def get_cases_by_user(self, user_id: UUID) -> List[CaseEntity]:
        cases = await self.case_repo.get_cases_by_user(user_id)

        return [
            CaseResponse(
                id=case.id,
                user_id=case.user_id,
                title=case.title,
                description=case.description,
                slug=case.slug,
                status=case.status,
                summary=case.summary,
                evidences=[],
                created_at=case.created_at,
                updated_at=case.updated_at,
            )
            for case in cases
        ]

    @handle_repo_exceptions
    async def update_case(
        self, case_id: UUID, user_id: UUID, case_request: UpdateCaseRequest
    ) -> CaseResponse:
        """Update a case by ID."""
        existing_case = await self.case_repo.get_case_by_id(case_id, user_id)

        updated_case = CaseEntity(
            id=case_id,
            user_id=user_id,
            title=case_request.title or existing_case.title,
            status=existing_case.status,
            description=case_request.description or existing_case.description,
            slug=case_request.slug or existing_case.slug,
            summary=case_request.summary or existing_case.summary,
        )

        return await self.case_repo.update_case(updated_case)

    @handle_repo_exceptions
    async def delete_case(self, case_id: UUID, user_id: UUID) -> None:
        """Delete a case by ID."""
        await self.case_repo.delete_case(case_id, user_id)

    # ----------------------------
    # CASE COLLECTIONS
    # ----------------------------
    @handle_repo_exceptions
    async def create_collection(
        self, collection_request: CreateCaseCollectionRequest, user_id: uuid.UUID
    ) -> CollectionResponse:

        collection_entity = CollectionEntity(
            id=uuid.uuid4(),
            user_id=user_id,
            title=collection_request.title,
            description=collection_request.description,
        )

        return await self.case_repo.create_collection(collection_entity)

    @handle_repo_exceptions
    async def get_collections_by_user(self, user_id: UUID) -> List[CollectionResponse]:
        """Retrieve all collections belonging to a user."""
        collections = await self.case_repo.get_collections_by_user(user_id)

        return [
            CollectionResponse(
                id=collection.id,
                user_id=collection.user_id,
                title=collection.title,
                description=collection.description,
                cases=[
                    CaseResponse(
                        id=case.id,
                        user_id=case.user_id,
                        title=case.title,
                        description=case.description,
                        slug=case.slug,
                        status=case.status,
                        summary=case.summary,
                        evidences=[],
                        created_at=case.created_at,
                        updated_at=case.updated_at,
                    )
                    for case in collection.cases
                ],
                created_at=collection.created_at,
                updated_at=collection.updated_at,
            )
            for collection in collections
        ]

    @handle_repo_exceptions
    async def get_collection(
        self, collection_id: UUID, user_id: UUID
    ) -> CollectionResponse:
        """Retrieve a collection by ID."""
        collection = await self.case_repo.get_collection_by_id(collection_id, user_id)

        return CollectionResponse(
            id=collection.id,
            user_id=collection.user_id,
            title=collection.title,
            description=collection.description,
            cases=[
                CaseResponse(
                    id=case.id,
                    user_id=case.user_id,
                    title=case.title,
                    description=case.description,
                    slug=case.slug,
                    status=case.status,
                    summary=case.summary,
                    evidences=[],
                    created_at=case.created_at,
                    updated_at=case.updated_at,
                )
                for case in collection.cases
            ],
            created_at=collection.created_at,
            updated_at=collection.updated_at,
        )

    @handle_repo_exceptions
    async def update_collection(
        self,
        collection_id: UUID,
        user_id: UUID,
        collection_request: UpdateCaseCollectionRequest,
    ) -> CollectionResponse:
        """Update an existing collection."""
        updated_entity = CollectionEntity(
            id=collection_id,
            user_id=user_id,
            title=collection_request.title,
            description=collection_request.description,
        )
        result_collection = await self.case_repo.update_collection(
            collection_id, user_id, updated_entity
        )

        return result_collection

    @handle_repo_exceptions
    async def delete_collection(self, collection_id: UUID, user_id: UUID) -> None:
        """Delete a collection by ID."""
        await self.case_repo.delete_collection(collection_id, user_id)

    @handle_repo_exceptions
    async def add_case_to_collection(
        self, collection_id: UUID, case_id: UUID, user_id: UUID
    ) -> None:
        """Add a case to a collection."""
        await self.case_repo.add_case_to_collection(collection_id, case_id, user_id)
