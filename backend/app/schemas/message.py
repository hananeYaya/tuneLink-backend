from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    conversation_id: UUID


class MessageResponseData(MessageBase):
    id: UUID
    sender_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
