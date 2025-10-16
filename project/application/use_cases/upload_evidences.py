import os
from typing import List

from fastapi import UploadFile

from project.application.interfaces.process_file_repository_interface import (
    ICaseRepository,
)
from project.celery_job.tasks import parse_evidence_file
from runtime_settings import UPLOAD_DIRECTORY


class UploadEvidencesUseCase:
    def __init__(self, file_repo: ICaseRepository):
        self.file_repo = file_repo

    async def execute(self, case_id: str, evidences: List[UploadFile]):
        saved_files = []
        try:
            for file in evidences:
                file_path = os.path.abspath(
                    os.path.join(UPLOAD_DIRECTORY, file.filename)
                )
                file_path = file_path.replace(
                    "\\", "/"
                )  # Normalize for Celery / cross-platform

                print(f"File path: {file_path}")

                # Read & write the uploaded file asynchronously
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                saved_files.append(file_path)

                parse_evidence_file.delay(file_path, case_id)

            return {"message": "Files uploaded successfully", "files": saved_files}

        except Exception as e:
            # Cleanup saved files in case of error
            for file_path in saved_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            raise e
