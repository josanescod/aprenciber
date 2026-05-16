import uuid
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.classroom import Classroom, ClassroomMember
from app.models.profile import Profile


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

    def get_by_teacher(self, db: Session, teacher_id: str) -> list[dict]:
        # pylint: disable=not-callable
        stmt = (
            select(Classroom, func.count(ClassroomMember.id).label("member_count"))  #
            .outerjoin(ClassroomMember, ClassroomMember.classroom_id == Classroom.id)
            .where(Classroom.teacher_id == teacher_id)
            .group_by(Classroom.id)
        )
        rows = db.execute(stmt).all()
        return [
            {
                **{
                    c.key: getattr(row.Classroom, c.key)
                    for c in Classroom.__table__.columns
                },
                "member_count": row.member_count,
            }
            for row in rows
        ]

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

    def get_members(self, db: Session, classroom_id: str) -> list[Profile]:
        stmt = (
            select(Profile)
            .join(ClassroomMember, ClassroomMember.student_id == Profile.id)
            .where(ClassroomMember.classroom_id == classroom_id)
        )
        return list(db.execute(stmt).scalars().all())

    def update(
        self, db: Session, *, classroom: Classroom, name: str, description: str | None
    ) -> Classroom:
        classroom.name = name
        classroom.description = description
        db.commit()
        db.refresh(classroom)
        return classroom

    def deactivate(self, db: Session, *, classroom: Classroom) -> Classroom:
        classroom.is_active = False
        db.commit()
        db.refresh(classroom)
        return classroom

    def remove_member(self, db: Session, *, classroom_id: str, student_id: str) -> None:
        stmt = select(ClassroomMember).where(
            ClassroomMember.classroom_id == classroom_id,
            ClassroomMember.student_id == student_id,
        )
        member = db.execute(stmt).scalar_one_or_none()
        if member:
            db.delete(member)
            db.commit()
