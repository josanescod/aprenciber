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

    def get_all(self, db: Session) -> list[Profile]:
        stmt = select(Profile).order_by(Profile.created_at.desc())
        return list(db.execute(stmt).scalars().all())

    def update_role(self, db: Session, *, profile: Profile, role: str) -> Profile:
        profile.role = role
        db.commit()
        db.refresh(profile)
        return profile

    def update_active(
        self, db: Session, *, profile: Profile, is_active: bool
    ) -> Profile:
        profile.is_active = is_active
        db.commit()
        db.refresh(profile)
        return profile

    def get_by_role(self, db: Session, role: str) -> list[Profile]:
        stmt = select(Profile).where(Profile.role == role).order_by(Profile.email)
        return list(db.execute(stmt).scalars().all())
