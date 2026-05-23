from sqlalchemy.orm import Session

from app.models.learning_event import (
    LearningEvent
)


class LearningRepository:

    @staticmethod
    def create_event(
        db: Session,
        topic: str,
        event_type: str
    ):

        event = LearningEvent(
            topic=topic,
            event_type=event_type
        )

        db.add(event)

        db.commit()

        db.refresh(event)

        return event

    @staticmethod
    def get_topic_events(
        db: Session,
        topic: str
    ):

        return (
            db.query(LearningEvent)

            .filter(
                LearningEvent.topic == topic
            )

            .all()
        )