from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_auth_user, require_admin
from app.schemas.scenario import ScenarioOut, ScenarioDetail, ScenarioAdminOut
from app.services.scenario_service import ScenarioService
from app.services.auth_provider import AuthenticatedUser

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


@router.get("/admin/all", response_model=list[ScenarioAdminOut])
def list_all_scenarios(
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_admin),
):
    service = ScenarioService(db)
    return service.list_all_scenarios()


@router.patch("/admin/{scenario_id}/toggle", response_model=ScenarioAdminOut)
def toggle_scenario_active(
    scenario_id: int,
    db: Session = Depends(get_db),
    _: AuthenticatedUser = Depends(require_admin),
):
    service = ScenarioService(db)
    return service.toggle_active(scenario_id)
