# Modèles pour les conversations et les messages
from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import User, Message  # noqa: F401


class Conversation(Base):
    """
    Modèle représentant une conversation entre deux utilisateurs.
    """

    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    participant1_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    participant2_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    participant1 = relationship(
        "User",
        foreign_keys=[participant1_id],
        back_populates="conversations_as_participant1",
    )
    participant2 = relationship(
        "User",
        foreign_keys=[participant2_id],
        back_populates="conversations_as_participant2",
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )
