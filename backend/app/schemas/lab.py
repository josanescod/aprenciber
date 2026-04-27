from datetime import datetime
from pydantic import BaseModel


class LabStartRequest(BaseModel):
    scenario_slug: str


class LabStartResponse(BaseModel):
    id: int
    scenario_id: int
    status: str
    containers_info: dict
    networks_info: dict
    terminal_url: str | None
    expires_at: datetime | None

    model_config = {"from_attributes": True}


class LabOut(BaseModel):
    id: int
    scenario_id: int
    status: str
    containers_info: dict
    networks_info: dict
    terminal_url: str | None
    expires_at: datetime | None

    model_config = {"from_attributes": True}
