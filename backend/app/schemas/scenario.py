from datetime import datetime
from pydantic import BaseModel


class ScenarioOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    difficulty: str
    tags: str | None

    model_config = {"from_attributes": True}


class ScenarioDetail(ScenarioOut):
    yaml_path: str
    created_at: datetime
