from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.repositories.profile_repository import ProfileRepository
from app.services.auth_provider import AuthenticatedUser


class ProfileService:
    def __init__(self) -> None:
        self.repository = ProfileRepository()

    def get_or_create_profile(
        self,
        db: Session,
        auth_user: AuthenticatedUser,
    ) -> Profile:
        profile = self.repository.get_by_id(db, auth_user.id)

        if profile is None:
            return self.repository.create(
                db,
                profile_id=auth_user.id,
                email=auth_user.email,
                full_name=auth_user.full_name,
            )

        if profile.email != auth_user.email or profile.full_name != auth_user.full_name:
            profile = self.repository.update_basic_fields(
                db,
                profile=profile,
                email=auth_user.email,
                full_name=auth_user.full_name,
            )

        return profile
