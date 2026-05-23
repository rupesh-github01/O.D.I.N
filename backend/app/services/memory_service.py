from sqlalchemy.orm import Session

from app.models.message import (
    Message
)

from app.models.memory_summary import (
    MemorySummary
)

from app.ai.llm.llm_service import (
    LLMService
)


class MemoryService:

    @staticmethod
    def summarize_conversation(
        db: Session,
        conversation_id: int
    ):

        messages = (
            db.query(Message)

            .filter(
                Message.conversation_id
                == conversation_id
            )

            .all()
        )

        conversation_text = "\n".join([
            f"{m.role}: {m.content}"
            for m in messages
        ])

        prompt = f"""
Summarize the following conversation into concise long-term memory.

Focus on:
- key concepts
- important knowledge
- conclusions
- learning insights

Conversation:
{conversation_text}
"""

        summary = (
            LLMService.generate_response(
                question=prompt,
                context=""
            )
        )

        memory_summary = MemorySummary(
            conversation_id=
            conversation_id,

            summary=summary
        )

        db.add(memory_summary)

        db.commit()

        db.refresh(memory_summary)

        return memory_summary