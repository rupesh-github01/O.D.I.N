from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:

    @staticmethod
    def create_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ):

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return message

    @staticmethod
    def get_recent_messages(
        db: Session,
        conversation_id: int,
        limit: int = 6
    ):

        return (
            db.query(Message)

            .filter(
                Message.conversation_id == conversation_id
            )

            .order_by(Message.created_at.desc())

            .limit(limit)

            .all()
        )