class RepositoryError(Exception):
    """Base exception for repository operations."""

    pass


class NotFoundError(RepositoryError):
    """Raised when a requested resource cannot be found in the database."""

    pass


class AccessDeniedError(RepositoryError):
    """Raised when a user tries to access or modify unauthorized data."""

    pass


class DuplicateAssociationError(RepositoryError):
    """Raised when the case is already part of the collection."""

    pass
