from sqlalchemy.orm import Session

from app.models.relationship import (
    Relationship
)


class RelationshipRepository:

    @staticmethod
    def create_relationship(
        db: Session,
        source_concept_id: int,
        target_concept_id: int,
        relationship_type: str
    ):

        relationship = Relationship(
            source_concept_id=source_concept_id,
            target_concept_id=target_concept_id,
            relationship_type=relationship_type
        )

        db.add(relationship)

        db.commit()

        db.refresh(relationship)

        return relationship