import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.classroom import Classroom, ClassroomMember


class ClassroomRepository:
    def create(
        self,
        db: Session,
        *,
        name: str,
        teacher_id: str,
        description: str | None = None,
    ) -> Classroom:
        classroom = Classroom(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            teacher_id=teacher_id,
            is_active=True,
        )
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom

    def get_by_teacher(self, db: Session, teacher_id: str) -> list[Classroom]:
        stmt = select(Classroom).where(Classroom.teacher_id == teacher_id)
        return list(db.execute(stmt).scalars().all())

    def get_by_id(self, db: Session, classroom_id: str) -> Classroom | None:
        stmt = select(Classroom).where(Classroom.id == classroom_id)
        return db.execute(stmt).scalar_one_or_none()

    def add_member(
        self, db: Session, *, classroom_id: str, student_id: str
    ) -> ClassroomMember:
        member = ClassroomMember(
            id=str(uuid.uuid4()),
            classroom_id=classroom_id,
            student_id=student_id,
        )
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    def is_member(self, db: Session, *, classroom_id: str, student_id: str) -> bool:
        stmt = select(ClassroomMember).where(
            ClassroomMember.classroom_id == classroom_id,
            ClassroomMember.student_id == student_id,
        )
        return db.execute(stmt).scalar_one_or_none() is not None
