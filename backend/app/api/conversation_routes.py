from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.conversation_service import (
    ConversationService
)

router = APIRouter()


@router.post("/conversations")
async def create_conversation(
    db: Session = Depends(get_db)
):

    conversation = (
        ConversationService
        .create_conversation(
            db=db
        )
    )

    return {
        "conversation_id":
        conversation.id
    }


@router.get("/conversations")
async def get_conversations(
    db: Session = Depends(get_db)
):

    conversations = (
        ConversationService
        .get_all_conversations(
            db=db
        )
    )

    return conversations