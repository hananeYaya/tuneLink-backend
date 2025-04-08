from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.conversations import Conversation  # noqa: F401


class Message(Base):
    """
    Modèle représentant un message dans une conversation.
    """

    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("conversations.id"))
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship(
        "User", back_populates="sent_messages", foreign_keys=[sender_id]
    )
    receiver = relationship(
        "User", back_populates="received_messages", foreign_keys=[receiver_id]
    )
