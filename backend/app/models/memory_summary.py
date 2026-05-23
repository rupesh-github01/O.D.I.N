from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from datetime import datetime

from app.db.database import Base


class MemorySummary(Base):

    __tablename__ = (
        "memory_summaries"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id")
    )

    summary = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )