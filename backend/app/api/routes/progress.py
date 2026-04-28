from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_auth_user
from app.dependencies.db import get_db
from app.models.scenario import Scenario
from app.models.user_progress import UserProgress
from app.services.auth_provider import AuthenticatedUser

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/me")
def get_my_progress(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Scenario, UserProgress)
        .outerjoin(
            UserProgress,
            (UserProgress.scenario_id == Scenario.id)
            & (UserProgress.user_id == auth_user.id),
        )
        .filter(Scenario.is_active == True)
        .order_by(Scenario.id.asc())
        .all()
    )

    return [
        {
            "scenario_id": scenario.id,
            "scenario_slug": scenario.slug,
            "scenario_title": scenario.title,
            "difficulty": scenario.difficulty,
            "success": progress.success if progress else False,
            "attempts": progress.attempts if progress else 0,
            "best_time_seconds": progress.best_time_seconds if progress else None,
            "last_attempt_at": progress.last_attempt_at if progress else None,
        }
        for scenario, progress in rows
    ]
