# Modèle pour les utilisateurs (musiciens)
from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import (  # noqa: F401
        Event,
        Conversation,
        Message,
        Notification,
        Participation,
        UserInstrument,
        UserGenre,
    )


class User(Base):
    """
    Modèle représentant un utilisateur de l'application.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    events: Mapped[List["Event"]] = relationship(back_populates="creator")
    participations: Mapped[List["Participation"]] = relationship(back_populates="user")
    instruments: Mapped[List["UserInstrument"]] = relationship(back_populates="user")
    genres: Mapped[List["UserGenre"]] = relationship(back_populates="user")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")

    # Relations pour les conversations et messages
    conversations_as_participant1: Mapped[List["Conversation"]] = relationship(
        back_populates="participant1", foreign_keys="Conversation.participant1_id"
    )
    conversations_as_participant2: Mapped[List["Conversation"]] = relationship(
        back_populates="participant2", foreign_keys="Conversation.participant2_id"
    )
    sent_messages: Mapped[List["Message"]] = relationship(back_populates="sender")
    received_messages: Mapped[List["Message"]] = relationship(
        back_populates="receiver", foreign_keys="Message.receiver_id"
    )
