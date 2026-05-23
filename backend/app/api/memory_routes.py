from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.memory_consolidation_service import (
    MemoryConsolidationService
)
from app.services.memory_service import (
    MemoryService
)

router = APIRouter()


@router.post("/memory/consolidate")
async def consolidate_memory(
    topic: str,
    db: Session = Depends(get_db)
):

    return (
        MemoryConsolidationService
        .consolidate_topic(
            db=db,
            topic=topic
        )
    )

@router.post(
    "/memory/summarize/{conversation_id}"
)
async def summarize_memory(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    summary = (
        MemoryService
        .summarize_conversation(
            db=db,
            conversation_id=
            conversation_id
        )
    )

    return {
        "summary":
        summary.summary
    }