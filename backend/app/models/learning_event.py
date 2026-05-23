from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from sqlalchemy.sql import func

from app.db.database import Base


class LearningEvent(Base):

    __tablename__ = "learning_events"

    id = Column(Integer, primary_key=True)

    topic = Column(String)

    event_type = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )