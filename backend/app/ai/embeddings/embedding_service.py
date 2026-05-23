from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    @staticmethod
    def generate_embedding(text: str):

        embedding = EmbeddingService.model.encode(text)

        return embedding.tolist()