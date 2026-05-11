from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.auth.supabase_auth_service import SupabaseAuthService
from app.services.auth_provider import AuthProvider, AuthenticatedUser
from app.dependencies.db import get_db
from app.repositories.profile_repository import ProfileRepository

supabase_auth_service = SupabaseAuthService()


def get_auth_provider() -> AuthProvider:
    return supabase_auth_service


def get_current_auth_user(
    authorization: str = Header(default=""),
    auth_provider: AuthProvider = Depends(get_auth_provider),
    db: Session = Depends(get_db),
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
        auth_user = auth_provider.get_user(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    # llegeix rol desde la base de dades
    profile = ProfileRepository().get_by_id(db, auth_user.id)
    if profile:
        auth_user.role = profile.role
        if not profile.is_active:  # usuaris desactivats no poden accedir a la app
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Compte desactivat",
            )

    return auth_user


# funcions per RBA
def require_student(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
) -> AuthenticatedUser:
    if auth_user.role not in ("student", "teacher", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accés denegat",
        )
    return auth_user


def require_teacher(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
) -> AuthenticatedUser:
    if auth_user.role not in ("teacher", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accés denegat — cal rol teacher o admin",
        )
    return auth_user


def require_admin(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
) -> AuthenticatedUser:
    if auth_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accés denegat — cal rol admin",
        )
    return auth_user
