from sqlalchemy.orm import Session

from app.models.memory_summary import (
    MemorySummary
)


class MemoryRetrievalService:

    @staticmethod
    def get_relevant_summaries(
        db: Session,
        conversation_id: int
    ):

        summaries = (

            db.query(MemorySummary)

            .filter(
                MemorySummary.conversation_id
                == conversation_id
            )

            .order_by(
                MemorySummary.created_at.desc()
            )

            .limit(3)

            .all()
        )

        return summaries