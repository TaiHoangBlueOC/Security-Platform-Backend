from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from project.application.dto.auth_dto import UserResponse
from project.application.dto.case_management_dto import CaseResponse


class CreateGroupRequest(BaseModel):
    name: str


class UpdateGroupRequest(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: UUID
    name: str
    created_by: UUID
    members: List[UserResponse]
    cases: List[CaseResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None
