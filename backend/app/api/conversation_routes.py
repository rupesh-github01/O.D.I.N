from fastapi import APIRouter, Depends
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
        ConversationService.create_conversation(
            db=db,
            title="New Conversation"
        )
    )

    return {
        "conversation_id": conversation.id
    }