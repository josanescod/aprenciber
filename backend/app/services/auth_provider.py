from dataclasses import dataclass
from typing import Protocol


@dataclass
class AuthenticatedUser:
    id: str
    email: str
    full_name: str | None = None
    role: str = "student"  # acces míni, rol amb menys permisos


class AuthProvider(Protocol):
    def get_user(self, token: str) -> AuthenticatedUser: ...
