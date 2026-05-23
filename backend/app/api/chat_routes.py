from fastapi import (
    APIRouter,
    Depends
)

from fastapi.responses import (
    StreamingResponse
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.chat_schema import (
    ChatRequest
)

from app.services.rag_service import (
    RAGService
)

router = APIRouter()


@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):

    return RAGService.ask_question(
        db=db,
        conversation_id=
        chat_request.conversation_id,
        question=
        chat_request.question
    )


@router.post("/chat/stream")
async def stream_chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):

    generator = (
        RAGService.stream_answer(
            db=db,
            conversation_id=
            chat_request.conversation_id,
            question=
            chat_request.question
        )
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )