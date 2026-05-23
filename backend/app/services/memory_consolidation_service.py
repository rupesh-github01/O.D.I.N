from sqlalchemy.orm import Session

from app.services.retrieval_service import (
    RetrievalService
)

from app.ai.llm.llm_service import (
    LLMService
)

from app.repositories.summary_repository import (
    SummaryRepository
)


class MemoryConsolidationService:

    @staticmethod
    def consolidate_topic(
        db: Session,
        topic: str
    ):

        # Step 1: Retrieve relevant knowledge
        retrieval_results = (
            RetrievalService.semantic_search(
                db=db,
                query=topic
            )
        )

        # Step 2: Build consolidation context
        context_parts = []

        for document, score in retrieval_results:

            context_parts.append(document)

        context = "\n\n".join(context_parts)

        # Step 3: Generate synthesized summary
        summary_prompt = f"""
You are consolidating long-term knowledge.

Generate:
- key insights
- concise understanding
- important concepts
- conceptual relationships

Topic:
{topic}

Knowledge:
{context}
"""

        summary = LLMService.generate_response(
            question=f"Summarize knowledge about {topic}",
            context=summary_prompt
        )

        # Step 4: Store summary
        stored_summary = (
            SummaryRepository.create_summary(
                db=db,
                topic=topic,
                summary_text=summary
            )
        )

        return {
            "topic": topic,
            "summary": stored_summary.summary_text
        }