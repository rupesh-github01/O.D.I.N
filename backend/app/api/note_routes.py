from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.note_schema import NoteCreate, NoteResponse
from app.services.note_service import NoteService
from app.db.session import get_db
from app.schemas.search_schema import SearchQuery
from app.services.retrieval_service import RetrievalService
from app.schemas.chat_schema import ChatRequest
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/notes", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):

    return NoteService.create_note(
        db=db,
        title=note.title,
        content=note.content
    )


@router.get("/notes", response_model=list[NoteResponse])
async def get_notes(
    db: Session = Depends(get_db)
):

    return NoteService.get_all_notes(db)

@router.post("/search")
async def semantic_search(
    search_query: SearchQuery
):

    results = RetrievalService.semantic_search(
        query=search_query.query
    )

    formatted_results = []

    for result in results:

        formatted_results.append({
            "score": result.score,
            "payload": result.payload
        })

    return formatted_results

@router.post("/chat")
async def chat_with_odin(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    return RAGService.ask_question(
        db=db,
        conversation_id=request.conversation_id,
        question=request.question
    )