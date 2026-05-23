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
    @staticmethod
    def generate_revision_recommendations(
        db: Session
    ):

        topics = (
            LearningRepository.get_all_topics(
                db=db
            )
        )

        recommendations = []

        for topic in topics:

            analysis = (
                LearningIntelligenceService
                .analyze_topic(
                    db=db,
                    topic=topic
                )
            )

            if (
                analysis.get(
                    "revision_recommended"
                )
            ):

                recommendations.append({
                    "topic": topic,
                    "days_since_review":
                    analysis[
                        "days_since_last_review"
                    ]
                })

        recommendations.sort(
            key=lambda x:
            x["days_since_review"],
            reverse=True
        )

        return recommendations