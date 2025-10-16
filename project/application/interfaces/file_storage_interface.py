from abc import ABC, abstractmethod
from typing import List


class IFileStorage(ABC):

    @abstractmethod
    async def upload_files(self, files) -> List[str]:
        """Uploads a file and returns its storage path or URL."""
        pass
