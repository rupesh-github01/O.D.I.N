from sqlalchemy.orm import Session

from app.repositories.graph_repository import (
    GraphRepository
)
import re


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
    # Extracting concept from question automatically
    @staticmethod
    def extract_query_concepts(
        question: str
    ):

        concepts = re.findall(
            r'\b[A-Z][a-zA-Z]+\b',
            question
        )

        return list(set(concepts))
    
    @staticmethod
    def build_graph_context(
        db: Session,
        question: str
    ):

        concepts = (
            GraphService.extract_query_concepts(
                question=question
            )
        )

        graph_context_parts = []

        for concept in concepts:

            related = (
                GraphRepository.get_related_concepts(
                    db=db,
                    concept_name=concept
                )
            )

            if related:

                graph_context_parts.append(
                    f"\nConcept: {concept}"
                )

                for relation in related:

                    graph_context_parts.append(
                        f"- {relation['relationship']} -> {relation['concept']}"
                    )

        return "\n".join(graph_context_parts)