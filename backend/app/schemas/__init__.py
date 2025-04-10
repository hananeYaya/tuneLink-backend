# app/schemas/__init__.py
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse, UserResponseData
from app.schemas.common import StatusCode, SuccessResponse, ErrorResponse
from app.schemas.message import (
    MessageCreate,
    MessageData,
    MessageResponse,
    MessageListResponse,
    MessageDeleteResponse,
)


__all__ = [
    # Utilisateurs
    "UserCreate", "UserResponse", "UserCreateResponse", "UserResponseData",
    # Communs
    "StatusCode", "SuccessResponse", "ErrorResponse",
      # Messages
    "MessageCreate", "MessageData", "MessageResponse", "MessageListResponse", "MessageDeleteResponse",
]