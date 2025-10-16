from typing import List

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)

from project.application.use_cases.upload_evidences import \
    UploadEvidencesUseCase
from project.infrastructure.celery_tasks.celery_app import CeleryJobDispatcher
from project.infrastructure.file_storage.local_storage_service import \
    LocalFileStorage
from project.presentation.dependencies.authentication_dependency import \
    get_user_info

router = APIRouter(prefix="/evidences", tags=["Upload Evidences"])


@router.post("/")
async def upload_evidences(
    case_id: str = Form(...),
    evidences: List[UploadFile] = File(...),
    user=Depends(get_user_info),
):
    file_storage = LocalFileStorage()
    job_dispatcher = CeleryJobDispatcher()
    use_case = UploadEvidencesUseCase(file_storage, job_dispatcher)

    try:
        await use_case.execute(case_id, evidences)

        return {"message": "Evidences uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
