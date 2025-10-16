import os
from typing import List

from project.application.interfaces.file_storage_interface import IFileStorage
from project.core.config import UPLOAD_DIRECTORY


class LocalFileStorage(IFileStorage):
    async def upload_files(self, files) -> List[str]:
        saved_files = []
        try:
            for file in files:
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

            return saved_files
        except Exception as e:
            # Cleanup saved files in case of error
            for file_path in saved_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            raise e
