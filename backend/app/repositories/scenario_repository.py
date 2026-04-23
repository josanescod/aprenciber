from sqlalchemy.orm import Session
from app.models.scenario import Scenario


class ScenarioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_active(self) -> list[Scenario]:
        return (
            self.db.query(Scenario)
            .filter(Scenario.is_active == True)
            .order_by(Scenario.created_at.asc())
            .all()
        )

    def get_by_id(self, scenario_id: int) -> Scenario | None:
        return (
            self.db.query(Scenario)
            .filter(Scenario.id == scenario_id, Scenario.is_active == True)
            .first()
        )

    def get_by_slug(self, slug: str) -> Scenario | None:
        return (
            self.db.query(Scenario)
            .filter(Scenario.slug == slug, Scenario.is_active == True)
            .first()
        )
