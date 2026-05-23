from sqlalchemy.orm import Session

from app.models.concept import Concept


class ConceptRepository:

    @staticmethod
    def get_or_create_concept(
        db: Session,
        name: str
    ):

        concept = (
            db.query(Concept)

            .filter(
                Concept.name == name
            )

            .first()
        )

        if concept:
            return concept

        concept = Concept(name=name)

        db.add(concept)

        db.commit()

        db.refresh(concept)

        return concept