from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.models.conversation import ConversationType


class ConversationCreate(BaseModel):
    name: str  # 👈 Ajouté
    type: ConversationType
    participant_ids: List[UUID]


class ConversationResponseData(BaseModel):
    id: UUID
    name: str  # 👈 Ajouté
    type: ConversationType
    created_at: datetime

    class Config:
        from_attributes = True  # Pour .model_validate()
