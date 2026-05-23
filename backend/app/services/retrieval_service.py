from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.retrieval.qdrant_service import QdrantService


class RetrievalService:

    @staticmethod
    def semantic_search(query: str):

        # Step 1: Convert query into embedding
        query_embedding = EmbeddingService.generate_embedding(
            text=query
        )

        # Step 2: Search similar vectors
        results = QdrantService.search_similar_notes(
            query_embedding=query_embedding
        )

        return results