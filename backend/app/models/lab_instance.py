from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class LabInstance(Base):
    __tablename__ = "lab_instances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("profiles.id"), nullable=False, index=True
    )
    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id"), nullable=False, index=True
    )

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="creating")
    network_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attacker_container_name: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    vulnerable_container_name: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    terminal_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    flag_value: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
