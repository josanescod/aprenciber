from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user_progress import UserProgress
from sqlalchemy import select
from app.models.scenario import Scenario


class UserProgressRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_and_scenario(
        self, user_id: str, scenario_id: int
    ) -> UserProgress | None:
        return (
            self.db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.scenario_id == scenario_id,
            )
            .first()
        )

    def upsert(
        self,
        user_id: str,
        scenario_id: int,
        success: bool,
        time_seconds: int | None = None,
    ) -> UserProgress:
        progress = self.get_by_user_and_scenario(user_id, scenario_id)

        if progress is None:
            progress = UserProgress(
                user_id=user_id,
                scenario_id=scenario_id,
                attempts=1,
                success=success,
                best_time_seconds=time_seconds if success else None,
                last_attempt_at=datetime.now(timezone.utc),
            )
            self.db.add(progress)
        else:
            progress.attempts += 1
            progress.last_attempt_at = datetime.now(timezone.utc)
            if success:
                progress.success = True
                if time_seconds is not None:
                    if progress.best_time_seconds is None:
                        progress.best_time_seconds = time_seconds
                    else:
                        progress.best_time_seconds = min(
                            progress.best_time_seconds, time_seconds
                        )

        self.db.commit()
        self.db.refresh(progress)
        return progress

    # mostrar progres de diferents usuaris
    def get_by_users(self, user_ids: list[str]) -> list[UserProgress]:
        if not user_ids:
            return []
        return (
            self.db.query(UserProgress).filter(UserProgress.user_id.in_(user_ids)).all()
        )
