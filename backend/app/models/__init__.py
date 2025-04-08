"""
Ce module contient tous les modèles SQLAlchemy de l'application.
"""

from app.models.base import Base
from app.models.user import User
from app.models.events import Event
from app.models.associations import Participation, UserInstrument, UserGenre
from app.models.conversations import Conversation
from app.models.messages import Message
from app.models.notifications import Notification

# Les autres modèles seront ajoutés ici au fur et à mesure de leur création

__all__ = [
    "Base",
    "User",
    "Event",
    "Participation",
    "UserInstrument",
    "UserGenre",
    "Conversation",
    "Message",
    "Notification",
]
