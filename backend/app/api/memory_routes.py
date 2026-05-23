from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.memory_consolidation_service import (
    MemoryConsolidationService
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