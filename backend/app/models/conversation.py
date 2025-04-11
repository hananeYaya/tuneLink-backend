from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
import enum

from app.database import Base

class ConversationType(str, enum.Enum):
    PRIVATE = "private"
    GROUP = "group"

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)  # 👈 Ajout du nom
    type = Column(Enum(ConversationType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete")
    participants = relationship("ConversationParticipant", back_populates="conversation", cascade="all, delete")
