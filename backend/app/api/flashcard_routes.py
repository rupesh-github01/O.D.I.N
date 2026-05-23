from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.flashcard_service import (
    FlashcardService
)

router = APIRouter()


@router.post(
    "/flashcards/generate/{topic}"
)
async def generate_flashcards(
    topic: str,
    db: Session = Depends(get_db)
):

    flashcards = (
        FlashcardService
        .generate_flashcards(
            db=db,
            topic=topic
        )
    )

    return flashcards