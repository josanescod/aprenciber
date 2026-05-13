from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClassroomCreate(BaseModel):
    name: str
    description: str | None = None


class ClassroomResponse(BaseModel):
    id: str
    name: str
    description: str | None
    teacher_id: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AddMemberRequest(BaseModel):
    student_id: str


class MemberResponse(BaseModel):
    id: str
    classroom_id: str
    student_id: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)
