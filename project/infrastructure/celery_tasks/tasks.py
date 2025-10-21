from project.application.use_cases.parse_evidence import ParseEvidencesUseCase
from project.dependencies.database_dependency import get_sync_db
from project.infrastructure.celery_tasks.celery_app import celery
from project.infrastructure.repositories.evidence_repository import EvidenceRepository


@celery.task(name="parse_evidence_file")
def parse_evidence_file(payload: dict):
    """
    Celery background task to parse uploaded evidence files.
    """
    print(f"Receiving payload: {payload}")
    db = get_sync_db()
    repo = EvidenceRepository(db)

    case_id = payload["case_id"]
    file_path = payload["file_path"]

    use_case = ParseEvidencesUseCase(
        evidence_repository=repo,
    )

    use_case.execute(case_id=case_id, file_path=file_path)
