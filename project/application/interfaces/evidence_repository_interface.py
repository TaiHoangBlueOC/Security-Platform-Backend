from abc import ABC, abstractmethod
from typing import List, Optional

from project.domain.entities import EvidenceEntity, MessageEntity


class IEvidenceRepository(ABC):
    # --- Synchronous Methods ---
    @abstractmethod
    def create(self, evidence: EvidenceEntity) -> EvidenceEntity:
        """Persist a new evidence entity."""
        pass

    @abstractmethod
    def update(self, evidence: EvidenceEntity) -> EvidenceEntity:
        """Update an existing evidence entity."""
        pass

    @abstractmethod
    def create_messages(self, messages: List[MessageEntity]) -> None:
        """Persist bulk message entities."""
        pass

    # --- Asynchronous Methods ---
    @abstractmethod
    async def get_by_id(self, evidence_id: str) -> Optional[EvidenceEntity]:
        """Retrieve an evidence entity by its ID."""
        pass

    @abstractmethod
    async def list_by_case_id(self, case_id: str) -> List[EvidenceEntity]:
        """List all evidences associated with a given case."""
        pass

    @abstractmethod
    async def delete(self, evidence_id: str) -> None:
        """Delete an evidence by its ID."""
        pass
