from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from qdrant_client.models import PointStruct


client = QdrantClient(
    host="localhost",
    port=6333
)


class QdrantService:

    COLLECTION_NAME = "odin_notes"

    @staticmethod
    def create_collection():

        collections = client.get_collections().collections

        existing = [
            collection.name
            for collection in collections
        ]

        if QdrantService.COLLECTION_NAME not in existing:

            client.create_collection(
                collection_name=QdrantService.COLLECTION_NAME,

                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )
    
    @staticmethod
    def insert_note_embedding(
        note_id: int,
        title: str,
        content: str,
        embedding: list[float]
    ):

        client.upsert(
            collection_name=QdrantService.COLLECTION_NAME,

            points=[
                PointStruct(
                    id=note_id,

                    vector=embedding,

                    payload={
                        "note_id": note_id,
                        "title": title,
                        "content": content
                    }
                )
            ]
        )

    @staticmethod
    def search_similar_notes(
        query_embedding: list[float],
        limit: int = 5
    ):

        results = client.query_points(
            collection_name=QdrantService.COLLECTION_NAME,

            query=query_embedding,

            limit=limit
        )

        return results.points