from sqlalchemy.orm import Session

from app.models.note import Note

from app.models.flashcard import (
    Flashcard
)

from app.ai.llm.llm_service import (
    LLMService
)


class FlashcardService:

    @staticmethod
    def generate_flashcards(
        db: Session,
        topic: str
    ):

        notes = (

            db.query(Note)

            .filter(
                Note.title.ilike(
                    f"%{topic}%"
                )
            )

            .all()
        )

        combined_notes = "\n\n".join([
            note.content
            for note in notes
        ])

        prompt = f"""
Generate 5 high-quality flashcards.

Rules:
- focus on conceptual understanding
- avoid trivial memorization
- use concise answers

Return format:

Q: ...
A: ...

Notes:
{combined_notes}
"""

        response = (
            LLMService.generate_response(
                question=prompt,
                context=""
            )
        )

        flashcards = []

        card_blocks = (
            response.split("Q:")
        )

        for block in card_blocks:

            if "A:" not in block:
                continue

            parts = block.split("A:")

            question = (
                parts[0].strip()
            )

            answer = (
                parts[1].strip()
            )

            flashcard = Flashcard(
                question=question,
                answer=answer,
                topic=topic
            )

            db.add(flashcard)

            flashcards.append(
                flashcard
            )

        db.commit()

        return flashcards