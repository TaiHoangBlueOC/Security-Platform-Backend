from typing import List, Optional

from sqlalchemy import insert

from project.application.interfaces.evidence_repository_interface import (
    IEvidenceRepository,
)
from project.domain.entities import EvidenceEntity, MessageEntity
from project.infrastructure.database.models import EvidenceModel, MessageModel


class EvidenceRepository(IEvidenceRepository):
    def __init__(self, session):
        self.session = session

    def create(self, evidence: EvidenceEntity) -> EvidenceEntity:
        db_evidence = EvidenceModel(
            id=evidence.id,
            case_id=evidence.case_id,
            source=evidence.source,
            status=evidence.status,
            format=evidence.format,
        )
        self.session.add(db_evidence)
        self.session.commit()
        self.session.refresh(db_evidence)

        evidence.id = db_evidence.id
        evidence.created_at = db_evidence.created_at
        evidence.updated_at = db_evidence.updated_at
        return evidence

    def update(self, evidence: EvidenceEntity) -> EvidenceEntity:
        db_evidence = (
            self.session.query(EvidenceModel).filter_by(id=evidence.id).first()
        )
        if not db_evidence:
            raise ValueError(f"Evidence with id={evidence.id} not found")

        # Update fields
        db_evidence.case_id = evidence.case_id
        db_evidence.source = evidence.source
        db_evidence.status = evidence.status
        db_evidence.format = evidence.format

        self.session.commit()
        self.session.refresh(db_evidence)

        # Reflect updated data back into domain entity
        evidence.updated_at = db_evidence.updated_at
        return evidence

    # def create_messages(self, messages: List[MessageEntity]) -> None:
    #     if not messages:
    #         return
    #
    #     db_messages = [
    #         MessageModel(
    #             id=message.id,
    #             evidence_id=message.evidence_id,
    #             sender=message.sender,
    #             receiver=message.receiver,
    #             payload=message.payload,
    #             status=message.status,
    #             embeddings=message.embeddings,
    #         )
    #         for message in messages
    #     ]
    #
    #     self.session.bulk_save_objects(db_messages)
    #     self.session.commit()

    def create_messages(self, messages: List[MessageEntity]) -> None:
        if not messages:
            return

        data = [
            {
                "id": message.id,
                "evidence_id": message.evidence_id,
                "sender": message.sender,
                "receiver": message.receiver,
                "payload": message.payload,
                "status": message.status,
                "embeddings": message.embeddings,
            }
            for message in messages
        ]

        stmt = insert(MessageModel).values(data)
        self.session.execute(stmt)
        self.session.commit()

    async def get_by_id(self, evidence_id: str) -> Optional[EvidenceEntity]:
        pass

    async def list_by_case_id(self, case_id: str) -> List[EvidenceEntity]:
        pass

    async def delete(self, evidence_id: str) -> None:
        pass
