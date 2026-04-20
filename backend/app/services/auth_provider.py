from dataclasses import dataclass
from typing import Protocol


@dataclass
class AuthenticatedUser:
    id: str
    email: str
    full_name: str | None = None


class AuthProvider(Protocol):
    def get_user(self, token: str) -> AuthenticatedUser: ...
