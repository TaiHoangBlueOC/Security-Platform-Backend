import csv
import os
import uuid

from celery import Celery
from sqlalchemy.orm import Session

from project.domain.enums import EvidenceStatus
from project.infrastructure.database.models import EvidenceModel, MessageModel
from project.infrastructure.database.session import SessionLocal
from runtime_settings import CELERY_BROKER_URL, CELERY_NAME, CELERY_RESULT_BACKEND

celery = Celery(
    main=CELERY_NAME,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery.task(name="parse_evidence_file")
def parse_evidence_file(file_path: str, case_id: str):
    """
    Celery task to parse uploaded evidence files.
    """

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    db: Session = SessionLocal()
    buffer = []
    batch_size = 500
    total = 0

    # Create Evidence record with status "Processing"
    evidence = EvidenceModel(
        id=uuid.uuid4(),
        case_id=case_id,
        file_path=file_path,
        status=EvidenceStatus.PROCESSING,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    print(f"Started parsing file: {file_path}")

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                message = MessageModel(
                    id=uuid.uuid4(),
                    evidence_id=evidence.id,
                    status=EvidenceStatus.PROCESSING,
                    sender=row["sender"],
                    receiver=row["receiver"],
                    payload=row["payload"],
                )
                buffer.append(message)

                if len(buffer) >= batch_size:
                    db.bulk_save_objects(buffer)
                    db.commit()

                    total += len(buffer)
                    print(f"✅ Inserted {len(buffer)} messages")

                    buffer.clear()

            # Final batch buffer:
            db.bulk_save_objects(buffer)
            db.commit()
            total += len(buffer)
            print(f"✅ Inserted {len(buffer)} messages")

        # Update Evidence status to "Parsed"
        evidence.status = EvidenceStatus.PARSED
        db.commit()

        return {
            "message": f"Parsed {total} rows successfully from {os.path.basename(file_path)}",
            "total_rows": total,
        }

    except Exception as e:
        db.rollback()
        evidence.status = EvidenceStatus.FAILED
        db.commit()
        return {"error": str(e)}

    finally:
        db.close()
