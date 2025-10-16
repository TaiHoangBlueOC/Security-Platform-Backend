from enum import Enum


class CaseStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"


class EvidenceStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PARSED = "parsed"
    FAILED = "failed"


class MessageStatus(str, Enum):
    PROCESSING = "processing"
    EMBEDDED = "embedded"
