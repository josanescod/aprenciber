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
    member_count: int = 0  # nombre estudiants per aula
    model_config = ConfigDict(from_attributes=True)


class AddMemberRequest(BaseModel):
    student_id: str


class MemberResponse(BaseModel):
    id: str
    classroom_id: str
    student_id: str
    joined_at: datetime
    model_config = ConfigDict(from_attributes=True)


# esquema per mostrar alumnes
class StudentResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


# esquema de progrés
class StudentProgressResponse(BaseModel):
    student_id: str
    student_email: str
    student_name: str | None
    scenario_id: int
    attempts: int
    success: bool
    last_attempt_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


# esquema per editar aules
class ClassroomUpdate(BaseModel):
    name: str
    description: str | None = None
