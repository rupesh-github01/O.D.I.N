from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from sqlalchemy.sql import func

from app.db.database import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )