from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.db.database import Base


class Relationship(Base):

    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)

    source_concept_id = Column(
        Integer,
        ForeignKey("concepts.id")
    )

    target_concept_id = Column(
        Integer,
        ForeignKey("concepts.id")
    )

    relationship_type = Column(String)