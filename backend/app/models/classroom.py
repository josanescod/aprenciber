from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.base import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    teacher_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("profiles.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class ClassroomMember(Base):
    __tablename__ = "classroom_members"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    classroom_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("classrooms.id"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(255), ForeignKey("profiles.id"), nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
