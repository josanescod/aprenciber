from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class UserMeResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserListItem(BaseModel):
    id: str
    email: str
    full_name: str | None
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserRoleUpdate(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        allowed = {"student", "teacher", "admin"}
        if v not in allowed:
            raise ValueError(f"Rol no vàlid. Allowed: {allowed}")
        return v
