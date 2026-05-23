from sqlalchemy.orm import Session

from app.repositories.graph_repository import (
    GraphRepository
)


class GraphService:

    @staticmethod
    def explore_concept(
        db: Session,
        concept_name: str
    ):

        related_concepts = (
            GraphRepository.get_related_concepts(
                db=db,
                concept_name=concept_name
            )
        )

        return {
            "concept": concept_name,
            "related_concepts": related_concepts
        }