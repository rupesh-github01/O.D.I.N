from sentence_transformers import (
    CrossEncoder
)


class Reranker:

    model = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    @staticmethod
    def rerank(
        query: str,
        documents: list[dict],
        top_k: int = 5
    ):

        pairs = [
        [query, doc["content"]]
        for doc in documents
        ]

        scores = Reranker.model.predict(
            pairs
        )

        ranked = list(
            zip(
                documents,
                scores
            )
        )

        ranked.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]