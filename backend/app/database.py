# Configuration de la connexion à la base de données
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base

# Utiliser une URL de connexion depuis la configuration
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db/mobile_musician"

# Création du moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fabrique de sessions de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Fonction utilitaire pour obtenir une session de base de données.
    Utilisée comme dépendance FastAPI.

    Yields:
        Session: Une session de base de données SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
