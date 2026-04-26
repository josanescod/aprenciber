from sqlalchemy.orm import Session
from app.models.lab_instance import LabInstance


class LabInstanceRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, lab: LabInstance) -> LabInstance:
        self.db.add(lab)
        self.db.commit()
        self.db.refresh(lab)
        return lab

    def get_by_id(self, lab_id: int) -> LabInstance | None:
        return self.db.query(LabInstance).filter(LabInstance.id == lab_id).first()

    def get_active_by_user(self, user_id: str) -> list[LabInstance]:
        return (
            self.db.query(LabInstance)
            .filter(
                LabInstance.user_id == user_id,
                LabInstance.status.in_(["creating", "running"]),
            )
            .all()
        )

    def update(self, lab: LabInstance) -> LabInstance:
        self.db.commit()
        self.db.refresh(lab)
        return lab
