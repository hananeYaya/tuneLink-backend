from fastapi import APIRouter
from app.api.endpoints import message  
from app.api.endpoints import users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
#api_router.include_router(message.router, prefix="/messagerie", tags=["Messagerie"])