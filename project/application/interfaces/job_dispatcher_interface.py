from abc import ABC, abstractmethod
from typing import Any


class IJobDispatcher(ABC):
    @abstractmethod
    def dispatch(self, job_name: str, payload: dict[str, Any]) -> None:
        """Send a background job to be processed later."""
        pass
