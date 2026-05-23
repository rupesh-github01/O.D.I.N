from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey
)

from app.db.database import Base


class NoteChunk(Base):

    __tablename__ = "note_chunks"

    id = Column(Integer, primary_key=True)

    note_id = Column(
        Integer,
        ForeignKey("notes.id")
    )

    chunk_index = Column(Integer)

    chunk_text = Column(Text)