from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.learning_repository import (
    LearningRepository
)


class LearningIntelligenceService:

    @staticmethod
    def analyze_topic(
        db: Session,
        topic: str
    ):

        events = (
            LearningRepository.get_topic_events(
                db=db,
                topic=topic
            )
        )

        if not events:

            return {
                "topic": topic,
                "status": "No learning history found."
            }

        last_event = max(
            events,
            key=lambda x: x.created_at
        )

        days_since_review = (
            datetime.utcnow()
            - last_event.created_at.replace(
                tzinfo=None
            )
        ).days

        revision_needed = (
            days_since_review >= 7
        )

        return {
            "topic": topic,
            "total_learning_events": len(events),
            "days_since_last_review": days_since_review,
            "revision_recommended": revision_needed
        }