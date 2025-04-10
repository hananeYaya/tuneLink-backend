# app/schemas/__init__.py
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse, UserResponseData
from app.schemas.common import StatusCode, SuccessResponse, ErrorResponse


__all__ = [
    # Utilisateurs
    "UserCreate", "UserResponse", "UserCreateResponse", "UserResponseData",
    # Communs
    "StatusCode", "SuccessResponse", "ErrorResponse"
]