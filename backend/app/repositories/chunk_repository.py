from sqlalchemy.orm import Session

from app.models.note_chunk import NoteChunk


class ChunkRepository:

    @staticmethod
    def create_chunk(
        db: Session,
        note_id: int,
        chunk_index: int,
        chunk_text: str
    ):

        chunk = NoteChunk(
            note_id=note_id,
            chunk_index=chunk_index,
            chunk_text=chunk_text
        )

        db.add(chunk)

        db.commit()

        db.refresh(chunk)

        return chunk
    @staticmethod
    def keyword_search_chunks(
        db: Session,
        query: str,
        limit: int = 5
    ):

        results = (
            db.query(NoteChunk)

            .filter(
                NoteChunk.chunk_text.ilike(
                    f"%{query}%"
                )
            )

            .limit(limit)

            .all()
        )

        return results