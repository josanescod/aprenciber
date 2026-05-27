from supabase import Client, create_client

from app.core.config import settings
from app.services.auth_provider import AuthProvider, AuthenticatedUser


class SupabaseAuthService(AuthProvider):
    def __init__(self) -> None:
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_publishable_key,
        )
        self.admin_client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
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

    def create_user(
        self, email: str, password: str, full_name: str | None = None
    ) -> AuthenticatedUser:
        response = self.admin_client.auth.admin.create_user(
            {
                "email": email,
                "password": password,
                "user_metadata": {"full_name": full_name},
                "email_confirm": True,
            }
        )
        user = response.user
        if user is None:
            raise ValueError("No s'ha pogut crear l'usuari")
        return AuthenticatedUser(
            id=user.id,
            email=user.email,
            full_name=full_name,
        )

    # Esborrar usuaris-estudiants
    def delete_user(self, user_id: str) -> None:
        self.admin_client.auth.admin.delete_user(user_id)
