from project.infrastructure.exceptions.exceptions import (
    AccessDeniedError,
    DuplicateAssociationError,
    NotFoundError,
)


class BaseAppException(Exception):
    """Base exception for our application"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(BaseAppException):
    """Raised when a requested resource is not found"""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class AuthenticationException(BaseAppException):
    """Raised for authentication failures"""

    def __init__(self, message: str):
        super().__init__(message, status_code=401)


class UnauthorizedAccessException(BaseAppException):
    """Raised for authentication failures"""

    def __init__(self, message: str):
        super().__init__(message, status_code=401)


class ResourceConflictException(BaseAppException):
    """Raised when a resource conflict occurs (e.g., username or email already exists)"""

    def __init__(self, message: str = "Resource already exists."):
        super().__init__(message, status_code=409)


def handle_repo_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AccessDeniedError as e:
            raise UnauthorizedAccessException(str(e))
        except DuplicateAssociationError as e:
            raise ResourceConflictException(str(e))
        except NotFoundError as e:
            raise ResourceNotFoundException(str(e))

    return wrapper
