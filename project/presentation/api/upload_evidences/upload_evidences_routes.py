from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from project.application.use_cases.upload_evidences import UploadEvidencesUseCase
from project.infrastructure.database.session import get_async_db
from project.infrastructure.repositories.case_repository import CaseRepository
from project.presentation.dependencies.authentication_dependency import get_user_info

router = APIRouter(prefix="/evidences", tags=["Upload Evidences"])


@router.post("/")
async def upload_evidences(
    case_id: str = Form(...),
    evidences: List[UploadFile] = File(...),
    db=Depends(get_async_db),
    user=Depends(get_user_info),
):
    repo = CaseRepository(db)
    use_case = UploadEvidencesUseCase(repo)

    try:
        await use_case.execute(case_id, evidences)

        return {"message": "Evidences uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
