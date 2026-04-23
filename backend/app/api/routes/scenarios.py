from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_auth_user
from app.schemas.scenario import ScenarioOut, ScenarioDetail
from app.services.scenario_service import ScenarioService

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.get("", response_model=list[ScenarioOut])
def list_scenarios(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_auth_user),
):
    service = ScenarioService(db)
    return service.list_active_scenarios()


@router.get("/{scenario_id}", response_model=ScenarioDetail)
def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_auth_user),
):
    service = ScenarioService(db)
    return service.get_scenario(scenario_id)
