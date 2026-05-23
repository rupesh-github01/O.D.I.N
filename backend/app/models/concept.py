from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.db.database import Base


class Concept(Base):

    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        unique=True,
        index=True
    )