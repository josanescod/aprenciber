from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import require_teacher
from app.dependencies.db import get_db
from app.schemas.classroom import (
    ClassroomCreate,
    ClassroomResponse,
    AddMemberRequest,
    MemberResponse,
    StudentResponse,
    StudentProgressResponse,
    ClassroomUpdate,
)
from app.services.auth_provider import AuthenticatedUser
from app.repositories.classroom_repository import ClassroomRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.user_progress_repository import UserProgressRepository

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


@router.get("/{classroom_id}/members", response_model=list[StudentResponse])
def list_members(
    classroom_id: str,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> list[StudentResponse]:
    repo = ClassroomRepository()
    classroom = repo.get_by_id(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="No s'ha trobat l'aula")
    if classroom.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="No ets el professor d'aquesta aula"
        )
    return repo.get_members(db, classroom_id=classroom_id)


@router.get("/{classroom_id}/progress", response_model=list[StudentProgressResponse])
def get_classroom_progress(
    classroom_id: str,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> list[StudentProgressResponse]:
    repo = ClassroomRepository()
    classroom = repo.get_by_id(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Aula no trobada")
    if classroom.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="No ets el professor d'aquesta aula"
        )
    members = repo.get_members(db, classroom_id=classroom_id)
    if not members:
        return []
    student_ids = [m.id for m in members]
    student_map = {m.id: m for m in members}
    progress_repo = UserProgressRepository(db)
    all_progress = progress_repo.get_by_users(student_ids)
    return [
        StudentProgressResponse(
            student_id=p.user_id,
            student_email=student_map[p.user_id].email,
            student_name=student_map[p.user_id].full_name,
            scenario_id=p.scenario_id,
            attempts=p.attempts,
            success=p.success,
            last_attempt_at=p.last_attempt_at,
        )
        for p in all_progress
        if p.user_id in student_map
    ]


@router.patch("/{classroom_id}", response_model=ClassroomResponse)
def update_classroom(
    classroom_id: str,
    body: ClassroomUpdate,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> ClassroomResponse:
    repo = ClassroomRepository()
    classroom = repo.get_by_id(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Aula no trobada")
    if classroom.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="No ets el professor d'aquesta aula"
        )
    return repo.update(
        db, classroom=classroom, name=body.name, description=body.description
    )


@router.delete("/{classroom_id}", status_code=204)
def delete_classroom(
    classroom_id: str,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> None:
    repo = ClassroomRepository()
    classroom = repo.get_by_id(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Aula no trobada")
    if classroom.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="No ets el professor d'aquesta aula"
        )
    repo.deactivate(db, classroom=classroom)


@router.delete("/{classroom_id}/members/{student_id}", status_code=204)
def remove_member(
    classroom_id: str,
    student_id: str,
    current_user: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> None:
    repo = ClassroomRepository()
    classroom = repo.get_by_id(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Aula no trobada")
    if classroom.teacher_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="No ets el professor d'aquesta aula"
        )
    repo.remove_member(db, classroom_id=classroom_id, student_id=student_id)
