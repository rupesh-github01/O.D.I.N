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

        # Step 4: Semantic retrieval
        retrieval_results = (
            RetrievalService.semantic_search(
                query=question
            )
        )

        # Step 5: Build semantic context
        semantic_context_parts = []

        for result in retrieval_results:

            payload = result.payload

            semantic_context_parts.append(
                f"""
                Title: {payload['title']}

                Content:
                {payload['content']}
"""
            )

        semantic_context = "\n\n".join(
            semantic_context_parts
        )

        # Step 6: Graph context
        graph_context = (
            GraphService.build_graph_context(
                db=db,
                question=question
            )
        )

        # Step 7: Combined context
        final_context = f"""
            Conversation History:
            {conversation_text}

            Relevant Notes:
            {semantic_context}

            Knowledge Graph Context:
            {graph_context}
        """

        # Step 8: Generate answer
        answer = LLMService.generate_response(
            question=question,
            context=final_context
        )

        # Step 9: Store assistant response
        ConversationService.store_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=answer
        )

        return {
            "answer": answer,
            "conversation_context": conversation_context,
            "retrieved_context": semantic_context_parts
        }