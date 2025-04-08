# Modèle pour les notifications
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Notification(Base):
    """
    Modèle représentant une notification envoyée à un utilisateur.

    Attributes:
        id (UUID): ID unique de la notification
        user_id (UUID): ID de l'utilisateur
        title (str): Titre de la notification
        message (str): Message de la notification
        type (str): Type de notification (message, event, system)
        is_read (bool): Indique si la notification a été lue
        created_at (datetime): Date de création de la notification
        updated_at (datetime): Date de dernière mise à jour de la notification
    """

    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(50))  # event, message, system, etc.
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    user = relationship("User", back_populates="notifications")
