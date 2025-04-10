from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class MessageCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    content: str

class MessageData(BaseModel):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    code: int
    message: str
    data: MessageData

class MessageListResponse(BaseModel):
    code: int
    message: str
    data: List[MessageData]

class MessageDeleteResponse(BaseModel):
    code: int
    message: str
