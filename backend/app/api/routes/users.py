from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_auth_user, require_admin, require_teacher
from app.dependencies.db import get_db
from app.schemas.user import UserMeResponse, UserListItem
from app.services.profile_service import ProfileService
from app.services.auth_provider import AuthenticatedUser
from app.repositories.profile_repository import ProfileRepository

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
