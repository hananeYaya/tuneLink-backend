# Modèles d'association pour les relations many-to-many
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.events import Event  # noqa: F401


class Participation(Base):
    """
    Modèle pour la participation des utilisateurs aux événements.

    Attributes:
        user_id (UUID): ID de l'utilisateur
        event_id (UUID): ID de l'événement
        status (str): Statut de la participation (pending, accepted, rejected)
        role (str): Rôle dans l'événement (organizer, participant)
    """

    __tablename__ = "participations"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    role: Mapped[str] = mapped_column(String, nullable=False, default="participant")

    # Relations
    user: Mapped["User"] = relationship(back_populates="participations")
    event: Mapped["Event"] = relationship(back_populates="participations")


class UserInstrument(Base):
    """
    Modèle pour l'association entre utilisateurs et instruments.

    Attributes:
        user_id (UUID): ID de l'utilisateur
        instrument (str): Nom de l'instrument
        level (str): Niveau de maîtrise (beginner, intermediate, advanced, expert)
    """

    __tablename__ = "user_instruments"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    instrument: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(String, nullable=False, default="intermediate")

    # Relations
    user: Mapped["User"] = relationship(back_populates="instruments")


class UserGenre(Base):
    """
    Modèle pour l'association entre utilisateurs et genres musicaux.

    Attributes:
        user_id (UUID): ID de l'utilisateur
        genre (str): Nom du genre musical
        preference (str): Niveau de préférence (favorite, like, neutral)
    """

    __tablename__ = "user_genres"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    preference: Mapped[str] = mapped_column(String, nullable=False, default="neutral")

    # Relations
    user: Mapped["User"] = relationship(back_populates="genres")
