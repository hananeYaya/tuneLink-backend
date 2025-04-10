# /workspace/backend/app/models/__init__.py

from app.models.base import Base  # Ce fichier doit maintenant exister
from app.models.user import User  # Importe tes autres modèles ici
from app.models.message import Message  # <- Ajoute ce modèle



__all__ = ["Base", "User", "Message"]