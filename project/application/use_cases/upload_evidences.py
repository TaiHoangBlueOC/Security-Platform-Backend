from typing import List

from fastapi import UploadFile

from project.application.interfaces.file_storage_interface import IFileStorage
from project.application.interfaces.job_dispatcher_interface import \
    IJobDispatcher


class UploadEvidencesUseCase:
    def __init__(self, file_storage: IFileStorage, job_dispatcher: IJobDispatcher):
        self.file_storage = file_storage
        self.job_dispatcher = job_dispatcher

    async def execute(self, case_id: str, evidences: List[UploadFile]):
        # Save file to upload directory
        saved_files = await self.file_storage.upload_files(evidences)

        # Call background job to parse each file
        for file_path in saved_files:
            payload = {"case_id": case_id, "file_path": file_path}

            self.job_dispatcher.dispatch(
                job_name="parse_evidence_file", payload=payload
            )
