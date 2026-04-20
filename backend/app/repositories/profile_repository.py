from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.profile import Profile


class ProfileRepository:
    def get_by_id(self, db: Session, profile_id: str) -> Profile | None:
        stmt = select(Profile).where(Profile.id == profile_id)
        return db.execute(stmt).scalar_one_or_none()

    def create(
        self,
        db: Session,
        *,
        profile_id: str,
        email: str,
        full_name: str | None = None,
        role: str = "student",
    ) -> Profile:
        profile = Profile(
            id=profile_id,
            email=email,
            full_name=full_name,
            role=role,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    def update_basic_fields(
        self,
        db: Session,
        *,
        profile: Profile,
        email: str,
        full_name: str | None = None,
    ) -> Profile:
        profile.email = email
        profile.full_name = full_name
        db.commit()
        db.refresh(profile)
        return profile
