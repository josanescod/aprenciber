from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.scenario import Scenario
from app.repositories.scenario_repository import ScenarioRepository


class ScenarioService:

    def __init__(self, db: Session):
        self.repository = ScenarioRepository(db)

    def list_active_scenarios(self) -> list[Scenario]:
        return self.repository.get_all_active()

    def get_scenario(self, scenario_id: int) -> Scenario:
        scenario = self.repository.get_by_id(scenario_id)
        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scenario {scenario_id} not found",
            )
        return scenario
