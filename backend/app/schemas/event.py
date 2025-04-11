# backend/app/schemas/event.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.common import SuccessResponse, ErrorResponse

class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=2000)
    location: str = Field(..., min_length=3, max_length=200)
    event_date: datetime = Field(..., example="2025-06-15T19:30:00Z")

class EventCreate(EventBase):
    tags: Optional[List[str]] = Field(None, example=["jazz", "gratuit"])

class EventResponseData(EventBase):
    id: UUID
    organizer_id: UUID
    created_at: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True

class EventCreateResponse(SuccessResponse[EventResponseData]):
    code: int = 201
    message: str = "Événement créé avec succès"

class EventListResponse(SuccessResponse[List[EventResponseData]]):
    code: int = 200
    message: str = "Événements récupérés avec succès"

class EventError(ErrorResponse[None]):
    pass
