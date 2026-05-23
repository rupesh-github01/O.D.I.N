from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.retrieval.qdrant_service import QdrantService
from app.repositories.chunk_repository import (
    ChunkRepository
)
from sqlalchemy.orm import Session

class RetrievalService:

    @staticmethod
    def semantic_search(
        db: Session,
        query: str
    ):

        # Step 1: Vector retrieval
        query_embedding = (
            EmbeddingService.generate_embedding(
                text=query
            )
        )

        vector_results = (
            QdrantService.search_similar_notes(
                query_embedding=query_embedding
            )
        )

        # Step 2: Keyword retrieval
        keyword_results = (
            ChunkRepository.keyword_search_chunks(
                db=db,
                query=query
            )
        )

        return {
            "vector_results": vector_results,
            "keyword_results": keyword_results
        }