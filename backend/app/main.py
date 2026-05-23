from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import engine, Base
from app.models.note import Note

from app.api.note_routes import router as note_router

from app.ai.retrieval.qdrant_service import QdrantService
from app.models.note_chunk import NoteChunk

from app.models.conversation import Conversation
from app.models.message import Message

from app.api.conversation_routes import (
    router as conversation_router
)

from app.models.concept import Concept
from app.models.relationship import Relationship

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup logic
    QdrantService.create_collection()

    yield

    # Shutdown logic
    # future cleanup here


app = FastAPI(
    lifespan=lifespan
)

Base.metadata.create_all(bind=engine)

app.include_router(note_router)

app.include_router(conversation_router)


@app.get("/")
async def root():
    return {"message": "ODIN backend with database is alive"}