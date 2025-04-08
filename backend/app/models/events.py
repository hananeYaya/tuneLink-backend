# Modèle pour les événements musicaux
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.associations import Participation  # noqa: F401


class Event(Base):
    """
    Modèle pour les événements musicaux.

    Attributes:
        title (str): Titre de l'événement
        description (str): Description détaillée
        start_time (datetime): Date et heure de début
        end_time (datetime): Date et heure de fin
        location_lat (float): Latitude du lieu
        location_long (float): Longitude du lieu
        address (str): Adresse du lieu
        creator_id (UUID): ID de l'utilisateur créateur
        status (str): Statut de l'événement (planned, ongoing, completed, cancelled)
    """

    __tablename__ = "events"

    # Informations de base
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Dates
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)

    # Localisation
    location_lat: Mapped[float] = mapped_column(nullable=False)
    location_long: Mapped[float] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)

    # Relations
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    creator: Mapped["User"] = relationship(
        back_populates="created_events", foreign_keys=[creator_id]
    )

    # Statut
    status: Mapped[str] = mapped_column(String, nullable=False, default="planned")

    # Relations avec les participants
    participations: Mapped[List["Participation"]] = relationship(back_populates="event")
