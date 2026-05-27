from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_auth_user, require_admin, require_teacher
from app.dependencies.db import get_db
from app.schemas.user import (
    UserMeResponse,
    UserListItem,
    UserRoleUpdate,
    UserActiveUpdate,
    UserCreate,
)
from app.services.profile_service import ProfileService
from app.services.auth_provider import AuthenticatedUser
from app.repositories.profile_repository import ProfileRepository
from app.infrastructure.auth.supabase_auth_service import SupabaseAuthService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
def get_me(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
) -> UserMeResponse:
    service = ProfileService()
    profile = service.get_or_create_profile(db, auth_user)
    return UserMeResponse.model_validate(profile)


@router.get("/", response_model=list[UserListItem])
def list_users(
    _auth_user: AuthenticatedUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[UserListItem]:
    repo = ProfileRepository()
    return repo.get_all(db)


@router.patch("/{user_id}/role", response_model=UserListItem)
def update_user_role(
    user_id: str,
    body: UserRoleUpdate,
    current_user: AuthenticatedUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserListItem:
    repo = ProfileRepository()
    profile = repo.get_by_id(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    if profile.id == current_user.id and body.role != "admin":
        raise HTTPException(status_code=400, detail="No pots canviar el teu propi rol")
    return repo.update_role(db, profile=profile, role=body.role)


# desactivar usuaris
@router.patch("/{user_id}/active", response_model=UserListItem)
def update_user_active(
    user_id: str,
    body: UserActiveUpdate,
    current_user: AuthenticatedUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserListItem:
    repo = ProfileRepository()
    profile = repo.get_by_id(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    if profile.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="No pots desactivar el teu propi usuari"
        )
    return repo.update_active(db, profile=profile, is_active=body.is_active)


# creacio d'usuaris per part de l'admin
@router.post("/", response_model=UserListItem, status_code=201)
def create_user(
    body: UserCreate,
    _: AuthenticatedUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserListItem:
    supabase = SupabaseAuthService()
    try:
        auth_user = supabase.create_user(
            email=body.email,
            password=body.password,
            full_name=body.full_name,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creant usuari a Supabase: {e}"
        )
    repo = ProfileRepository()
    profile = repo.create(
        db,
        profile_id=auth_user.id,
        email=body.email,
        full_name=body.full_name,
        role=body.role,
    )
    return UserListItem.model_validate(profile)


@router.get("/by-role/{role}", response_model=list[UserListItem])
def list_users_by_role(
    role: str,
    _: AuthenticatedUser = Depends(require_teacher),
    db: Session = Depends(get_db),
) -> list[UserListItem]:
    repo = ProfileRepository()
    return repo.get_by_role(db, role=role)


@router.delete("/me", status_code=204)
def delete_my_account(
    auth_user: AuthenticatedUser = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
) -> None:
    if auth_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Només els students poden eliminar el seu compte",
        )
    repo = ProfileRepository()
    profile = repo.get_by_id(db, auth_user.id)
    if profile:
        repo.delete(db, profile=profile)
    supabase = SupabaseAuthService()
    supabase.delete_user(auth_user.id)
