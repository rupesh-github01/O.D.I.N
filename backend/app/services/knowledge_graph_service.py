import re

from sqlalchemy.orm import Session

from app.repositories.concept_repository import (
    ConceptRepository
)

from app.repositories.relationship_repository import (
    RelationshipRepository
)


class KnowledgeGraphService:

    @staticmethod
    def extract_concepts(text: str):

        # Temporary naive extraction
        # Later replaced with NLP/LLM extraction

        words = re.findall(
            r'\b[A-Z][a-zA-Z]+\b',
            text
        )

        unique_words = list(set(words))

        return unique_words

    @staticmethod
    def build_knowledge_graph(
        db: Session,
        text: str
    ):

        concepts = (
            KnowledgeGraphService.extract_concepts(
                text=text
            )
        )

        concept_objects = []

        # Create concepts
        for concept_name in concepts:

            concept = (
                ConceptRepository.get_or_create_concept(
                    db=db,
                    name=concept_name
                )
            )

            concept_objects.append(concept)

        # Create simple relationships
        for i in range(
            len(concept_objects) - 1
        ):

            RelationshipRepository.create_relationship(
                db=db,
                source_concept_id=concept_objects[i].id,
                target_concept_id=concept_objects[i + 1].id,
                relationship_type="related_to"
            )