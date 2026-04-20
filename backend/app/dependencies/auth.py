from fastapi import Depends, Header, HTTPException, status

from app.infrastructure.auth.supabase_auth_service import SupabaseAuthService
from app.services.auth_provider import AuthProvider, AuthenticatedUser


supabase_auth_service = SupabaseAuthService()


def get_auth_provider() -> AuthProvider:
    return supabase_auth_service


def get_current_auth_user(
    authorization: str = Header(default=""),
    auth_provider: AuthProvider = Depends(get_auth_provider),
) -> AuthenticatedUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    try:
        return auth_provider.get_user(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
