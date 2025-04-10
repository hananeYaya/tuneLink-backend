from sqlalchemy import Column, String, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


     # Relations
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_id]")
    received_messages = relationship("Message", back_populates="receiver", foreign_keys="[Message.receiver_id]")


   
