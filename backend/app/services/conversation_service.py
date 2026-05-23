from sqlalchemy.orm import Session

from app.repositories.conversation_repository import (
    ConversationRepository
)

from app.repositories.message_repository import (
    MessageRepository
)


class ConversationService:

    @staticmethod
    def create_conversation(
        db: Session,
        title: str
    ):

        return ConversationRepository.create_conversation(
            db=db,
            title=title
        )

    @staticmethod
    def store_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ):

        return MessageRepository.create_message(
            db=db,
            conversation_id=conversation_id,
            role=role,
            content=content
        )

    @staticmethod
    def get_recent_messages(
        db: Session,
        conversation_id: int
    ):

        return MessageRepository.get_recent_messages(
            db=db,
            conversation_id=conversation_id
        )