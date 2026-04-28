from sqlalchemy.orm import Session
from app.models.submission import Submission


class SubmissionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, submission: Submission) -> Submission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_by_lab(self, lab_id: int) -> list[Submission]:
        return (
            self.db.query(Submission)
            .filter(Submission.lab_instance_id == lab_id)
            .order_by(Submission.submitted_at.desc())
            .all()
        )

    def get_correct_by_user_and_scenario(
        self, user_id: str, scenario_id: int
    ) -> Submission | None:
        return (
            self.db.query(Submission)
            .filter(
                Submission.user_id == user_id,
                Submission.scenario_id == scenario_id,
                Submission.is_correct == True,
            )
            .first()
        )
