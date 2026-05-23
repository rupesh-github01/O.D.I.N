from sqlalchemy.orm import Session

from app.repositories.note_repository import NoteRepository

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.retrieval.qdrant_service import QdrantService
from app.ai.chunking.text_chunker import TextChunker
from app.repositories.chunk_repository import ChunkRepository


class NoteService:

    @staticmethod
    def create_note(
        db: Session,
        title: str,
        content: str
    ):

        # Step 1: Store original note
        note = NoteRepository.create_note(
            db=db,
            title=title,
            content=content
        )

        # Step 2: Chunk note
        chunks = TextChunker.chunk_text(
            text=content
        )

        # Step 3: Process each chunk
        for index, chunk_text in enumerate(chunks):

            # Store chunk in PostgreSQL
            chunk = ChunkRepository.create_chunk(
                db=db,
                note_id=note.id,
                chunk_index=index,
                chunk_text=chunk_text
            )

            # Generate embedding
            embedding = EmbeddingService.generate_embedding(
                text=chunk_text
            )

            # Store in Qdrant
            QdrantService.insert_note_embedding(
                note_id=chunk.id,
                title=title,
                content=chunk_text,
                embedding=embedding
            )

        return note
    @staticmethod
    def get_all_notes(db: Session):

        return NoteRepository.get_all_notes(db)