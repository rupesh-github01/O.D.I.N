from sqlalchemy.orm import Session

from app.services.retrieval_service import (
    RetrievalService
)

from app.ai.llm.llm_service import (
    LLMService
)

from app.services.conversation_service import (
    ConversationService
)

from app.services.graph_service import (
    GraphService
)

from app.repositories.learning_repository import (
    LearningRepository
)

from app.services.memory_retrieval_service import (
    MemoryRetrievalService
)


class RAGService:

    @staticmethod
    def ask_question(
        db: Session,
        conversation_id: int,
        question: str
    ):

        # Step 1: Store user message
        ConversationService.store_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=question
        )

        # Step 2: Retrieve recent conversation
        recent_messages = (
            ConversationService.get_recent_messages(
                db=db,
                conversation_id=conversation_id
            )
        )

        # Step 3: Build conversation context
        conversation_context = []

        for message in reversed(recent_messages):

            conversation_context.append(
                f"{message.role}: {message.content}"
            )

        conversation_text = "\n".join(
            conversation_context
        )

        # Step 4: Retrieve long-term memory summaries
        memory_summaries = (

            MemoryRetrievalService
            .get_relevant_summaries(
                db=db,
                conversation_id=conversation_id
            )
        )

        memory_context_parts = []

        for summary in memory_summaries:

            memory_context_parts.append(
                f"""
[Long-Term Memory Summary]

{summary.summary}
"""
            )

        memory_context = "\n\n".join(
            memory_context_parts
        )

        # Step 5: Semantic retrieval + reranking
        retrieval_results = (
            RetrievalService.semantic_search(
                db=db,
                query=question
            )
        )

        # Step 6: Build semantic context
        semantic_context_parts = []

        for doc, score in retrieval_results:

            semantic_context_parts.append(
                f"""
[Reranked Context]

Source:
{doc["source"]}

Relevance Score:
{score}

Content:
{doc["content"]}
"""
            )

        semantic_context = "\n\n".join(
            semantic_context_parts
        )

        # Step 7: Build citations
        citations = []

        for doc, score in retrieval_results:

            citations.append({
                "source": doc["source"],
                "score": float(score)
            })

        # Step 8: Graph context
        graph_context = (
            GraphService.build_graph_context(
                db=db,
                question=question
            )
        )

        # Step 9: Combined hierarchical context
        final_context = f"""
Conversation History:
{conversation_text}

Long-Term Memory:
{memory_context}

Relevant Notes:
{semantic_context}

Knowledge Graph Context:
{graph_context}
"""

        # Step 10: Generate answer
        answer = LLMService.generate_response(
            question=question,
            context=final_context
        )

        # Step 11: Store assistant response
        ConversationService.store_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=answer
        )

        # Step 12: Detect learning topic
        detected_topic = "General"

        graph_concepts = (
            GraphService.extract_query_concepts(
                question=question
            )
        )

        if graph_concepts:

            detected_topic = (
                graph_concepts[0]
            )

        # Step 13: Store learning event
        LearningRepository.create_event(
            db=db,
            topic=detected_topic,
            event_type="topic_revisited"
        )

        # Step 14: Return response
        return {
            "answer": answer,
            "citations": citations,
            "conversation_context": conversation_context,
            "retrieved_context": semantic_context_parts,
            "memory_context": memory_context_parts
        }

    @staticmethod
    def stream_answer(
        db: Session,
        conversation_id: int,
        question: str
    ):

        # Step 1: Retrieve long-term memory summaries
        memory_summaries = (

            MemoryRetrievalService
            .get_relevant_summaries(
                db=db,
                conversation_id=conversation_id
            )
        )

        memory_context_parts = []

        for summary in memory_summaries:

            memory_context_parts.append(
                f"""
[Long-Term Memory Summary]

{summary.summary}
"""
            )

        memory_context = "\n\n".join(
            memory_context_parts
        )

        # Step 2: Semantic retrieval
        retrieval_results = (
            RetrievalService.semantic_search(
                db=db,
                query=question
            )
        )

        # Step 3: Build semantic context
        semantic_context_parts = []

        for doc, score in retrieval_results:

            semantic_context_parts.append(
                f"""
[Reranked Context]

Source:
{doc["source"]}

Relevance Score:
{score}

Content:
{doc["content"]}
"""
            )

        semantic_context = "\n\n".join(
            semantic_context_parts
        )

        # Step 4: Graph context
        graph_context = (
            GraphService.build_graph_context(
                db=db,
                question=question
            )
        )

        # Step 5: Final hierarchical context
        final_context = f"""
Long-Term Memory:
{memory_context}

Relevant Notes:
{semantic_context}

Knowledge Graph Context:
{graph_context}
"""

        # Step 6: Stream response
        for chunk in (
            LLMService.stream_response(
                question=question,
                context=final_context
            )
        ):

            yield chunk