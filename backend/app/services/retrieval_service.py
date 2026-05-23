from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.retrieval.qdrant_service import QdrantService
from app.repositories.chunk_repository import (
    ChunkRepository
)
from sqlalchemy.orm import Session
from app.ai.reranking.reranker import (
    Reranker
)

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
                query_embedding=query_embedding,
                limit=10
            )
        )

        # Step 2: Keyword retrieval
        keyword_results = (
            ChunkRepository.keyword_search_chunks(
                db=db,
                query=query,
                limit=10
            )
        )

        # Step 3: Collect candidate documents
        candidate_documents = []

        # Vector candidates
        for result in vector_results:

            payload = result.payload

            candidate_documents.append(
                payload["content"]
            )

        # Keyword candidates
        for chunk in keyword_results:

            candidate_documents.append(
                chunk.chunk_text
            )

        # Remove duplicates
        candidate_documents = list(
            set(candidate_documents)
        )

        # Step 4: Rerank
        reranked_results = (
            Reranker.rerank(
                query=query,
                documents=candidate_documents,
                top_k=5
            )
        )

        return reranked_results