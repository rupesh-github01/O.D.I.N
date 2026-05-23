from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.learning_intelligence_service import (
    LearningIntelligenceService
)

router = APIRouter()


@router.get("/learning/analyze")
async def analyze_learning(
    topic: str,
    db: Session = Depends(get_db)
):

    return (
        LearningIntelligenceService
        .analyze_topic(
            db=db,
            topic=topic
        )
    )