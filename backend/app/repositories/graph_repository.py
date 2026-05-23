from sqlalchemy.orm import Session

from app.models.concept import Concept
from app.models.relationship import (
    Relationship
)


class GraphRepository:

    @staticmethod
    def get_related_concepts(
        db: Session,
        concept_name: str
    ):

        concept = (
            db.query(Concept)

            .filter(
                Concept.name == concept_name
            )

            .first()
        )

        if not concept:
            return []

        relationships = (
            db.query(Relationship)

            .filter(
                Relationship.source_concept_id
                == concept.id
            )

            .all()
        )

        related_concepts = []

        for relationship in relationships:

            target_concept = (
                db.query(Concept)

                .filter(
                    Concept.id
                    == relationship.target_concept_id
                )

                .first()
            )

            if target_concept:

                related_concepts.append({
                    "concept": target_concept.name,
                    "relationship": relationship.relationship_type
                })

        return related_concepts