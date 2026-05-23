from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.repositories.learning_repository import (
    LearningRepository
)

from app.services.learning_intelligence_service import (
    LearningIntelligenceService
)

router = APIRouter()


@router.get("/analytics/overview")
async def get_learning_overview(
    db: Session = Depends(get_db)
):

    topics = (
        LearningRepository.get_all_topics(
            db=db
        )
    )

    recommendations = (
        LearningIntelligenceService
        .generate_revision_recommendations(
            db=db
        )
    )

    return {
        "total_topics":
        len(topics),

        "revision_recommendations":
        recommendations,

        "revision_count":
        len(recommendations)
    }