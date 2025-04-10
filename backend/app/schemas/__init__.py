# Exporter les schémas pour qu'ils soient disponibles directement depuis app.schemas
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse, UserResponseData, UserError
from app.schemas.common import StatusCode, SuccessResponse, ErrorResponse
from app.schemas.auth import Token  # 👈 Nouveau schéma importé
# backend/app/schemas/__init__.py
from app.schemas.event import (
    EventCreate, EventResponseData, EventCreateResponse, EventListResponse, EventError
)




__all__ = [
    "UserCreate", 
    "UserResponse",
    "UserCreateResponse",
    "UserResponseData", 
    "UserError",
    "StatusCode",
    "SuccessResponse",
    "ErrorResponse",
    "Token"  # 👈 Nouveau schéma ajouté
    "EventCreate",
    "EventResponseData",
    "EventCreateResponse",
    "EventListResponse",
    "EventError"
]
