from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.db.database import Base


class Summary(Base):

    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True)

    topic = Column(String)

    summary_text = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )