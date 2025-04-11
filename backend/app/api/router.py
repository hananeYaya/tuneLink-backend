from fastapi import APIRouter
from app.api.endpoints import users, auth, events, messaging

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(events.router, prefix="/events", tags=["Événements"])
api_router.include_router(messaging.router, prefix="/messaging", tags=["Messagerie"])
