import csv
import os
import uuid

from project.application.interfaces.evidence_repository_interface import \
    IEvidenceRepository
from project.domain.entities import EvidenceEntity, MessageEntity
from project.domain.enums import EvidenceStatus


class ParseEvidencesUseCase:
    def __init__(
        self,
        evidence_repository: IEvidenceRepository,
    ):
        self.evidence_repository = evidence_repository

    def execute(self, case_id: str, file_path: str):
        """
        Celery task to parse uploaded evidence files.
        """

        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        buffer = []
        batch_size = 500
        total = 0

        # Create Evidence record with status "Processing"
        evidence_entity = EvidenceEntity(
            id=uuid.uuid4(),
            case_id=case_id,
            source=file_path,
            status=EvidenceStatus.PROCESSING,
            format="csv",
            metadata={"original_filename": os.path.basename(file_path)},
            attributes=["sender", "receiver", "payload"],
        )
        self.evidence_repository.create(evidence_entity)
        print(f"Started parsing file: {file_path}")

        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    message = MessageEntity(
                        id=uuid.uuid4(),
                        evidence_id=evidence_entity.id,
                        status=EvidenceStatus.PROCESSING,
                        sender=row["sender"],
                        receiver=row["receiver"],
                        payload=row["payload"],
                    )
                    buffer.append(message)

                    if len(buffer) >= batch_size:
                        self.evidence_repository.create_messages(buffer)

                        total += len(buffer)
                        print(f"✅ Inserted {len(buffer)} messages")

                        buffer.clear()

                # Final batch buffer:
                self.evidence_repository.create_messages(buffer)
                total += len(buffer)
                print(f"✅ Inserted {len(buffer)} messages")

            # Update Evidence status to "Parsed"
            evidence_entity.status = EvidenceStatus.PARSED
            self.evidence_repository.update(evidence_entity)

            return {
                "message": f"Parsed {total} rows successfully from {os.path.basename(file_path)}",
                "total_rows": total,
            }

        except Exception as e:
            evidence_entity.status = EvidenceStatus.FAILED
            self.evidence_repository.update(evidence_entity)
            return {"error": str(e)}
