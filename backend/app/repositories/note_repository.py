from sqlalchemy.orm import Session
from app.models.note import Note


class NoteRepository:

    @staticmethod
    def create_note(db: Session, title: str, content: str):

        note = Note(
            title=title,
            content=content
        )

        db.add(note)
        db.commit()
        db.refresh(note)

        return note

    @staticmethod
    def get_all_notes(db: Session):

        return db.query(Note).all()