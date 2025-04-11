# /workspace/backend/app/models/__init__.py
from app.models.base import Base
from app.models.user import User
from app.models.event import Event
from .conversation import Conversation  # ← ceci est nécessaire !!!
from .conversation_participant import ConversationParticipant
from .message import Message

__all__ = ["User", "Event", "Conversation", "ConversationParticipant", "Message"]
