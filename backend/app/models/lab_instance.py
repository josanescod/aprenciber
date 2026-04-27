from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class LabInstance(Base):
    __tablename__ = "lab_instances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("profiles.id"), nullable=False, index=True
    )
    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="running")
    containers_info: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    networks_info: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    terminal_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    terminal_pid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    flag_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
