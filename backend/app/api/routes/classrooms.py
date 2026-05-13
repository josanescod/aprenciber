from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import require_teacher
from app.dependencies.db import get_db
from app.schemas.classroom import (
    ClassroomCreate,
    ClassroomResponse,
    AddMemberRequest,
    MemberResponse,
)
from app.services.auth_provider import AuthenticatedUser
from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.profile_repository import ProfileRepository

router = APIRouter(prefix="/api/classrooms", tags=["classrooms"])


@router.post("/", response_model=ClassroomResponse, status_code=201)
def create_classroom(
    body: ClassroomCreate,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> ClassroomResponse:
    repo = ClassroomRepository()
    classroom = repo.create(
        db,
        name=body.name,
        description=body.description,
        teacher_id=current_user.id,
    )
    return ClassroomResponse.model_validate(classroom)


@router.get("/", response_model=list[ClassroomResponse])
def list_classrooms(
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> list[ClassroomResponse]:
    repo = ClassroomRepository()
    return repo.get_by_teacher(db, teacher_id=current_user.id)


@router.post("/{classroom_id}/members", response_model=MemberResponse, status_code=201)
def add_member(
    classroom_id: str,
    body: AddMemberRequest,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> MemberResponse:
    repo = ClassroomRepository()
    classroom = repo.get_by_id(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="No s'ha trobat l'aula.")
    if classroom.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="No ets el professor d'aquesta aula"
        )
    profile_repo = ProfileRepository()
    student = profile_repo.get_by_id(db, body.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="No s'ha trobat l'alumne")
    if student.role != "student":
        raise HTTPException(
            status_code=400, detail="Només es poden afegir alumnes a l'aula"
        )
    if repo.is_member(db, classroom_id=classroom_id, student_id=body.student_id):
        raise HTTPException(status_code=400, detail="L'alumne ja és membre de l'aula")
    return repo.add_member(db, classroom_id=classroom_id, student_id=body.student_id)
