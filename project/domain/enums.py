from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class CaseStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"


class EvidenceFormat(str, Enum):
    CSV = "csv"
    EXCEL = "excel"


class EvidenceStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PARSED = "parsed"
    FAILED = "failed"


class MessageStatus(str, Enum):
    PROCESSING = "processing"
    EMBEDDED = "embedded"
