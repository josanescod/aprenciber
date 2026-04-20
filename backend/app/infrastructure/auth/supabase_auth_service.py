from supabase import Client, create_client

from app.core.config import settings
from app.services.auth_provider import AuthProvider, AuthenticatedUser


class SupabaseAuthService(AuthProvider):
    def __init__(self) -> None:
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_publishable_key,
        )

    def get_user(self, token: str) -> AuthenticatedUser:
        response = self.client.auth.get_user(token)
        user = response.user

        if user is None:
            raise ValueError("Authenticated user not found")

        metadata = user.user_metadata or {}

        return AuthenticatedUser(
            id=user.id,
            email=user.email,
            full_name=metadata.get("full_name") or metadata.get("name"),
        )
