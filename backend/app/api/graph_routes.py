from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.graph_schema import (
    GraphQuery
)

from app.services.graph_service import (
    GraphService
)

router = APIRouter()


@router.post("/graph/explore")
async def explore_concept(
    query: GraphQuery,
    db: Session = Depends(get_db)
):

    return GraphService.explore_concept(
        db=db,
        concept_name=query.concept
    )