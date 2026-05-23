from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)

from datetime import datetime

from app.db.database import Base


class Flashcard(Base):

    __tablename__ = "flashcards"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text
    )

    answer = Column(
        Text
    )

    topic = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )