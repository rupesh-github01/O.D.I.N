from sqlalchemy.orm import Session

from app.models.summary import Summary


class SummaryRepository:

    @staticmethod
    def create_summary(
        db: Session,
        topic: str,
        summary_text: str
    ):

        summary = Summary(
            topic=topic,
            summary_text=summary_text
        )

        db.add(summary)

        db.commit()

        db.refresh(summary)

        return summary