from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from typing import Any, List, Dict
from datetime import datetime
import uuid
import shutil
import os

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserResponseData,
    UserError
)
from app.database import get_db
from app.core.security import get_password_hash

router = APIRouter()

UPLOAD_DIRECTORY = "app/static/profile_pictures"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post(
    "/register", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserCreateResponse,
    summary="Créer un nouveau compte utilisateur",
    description="Crée un nouveau compte utilisateur avec un nom d'utilisateur unique, une adresse email, un mot de passe, et une photo de profil optionnelle.",
    responses={
        201: {"description": "Utilisateur créé avec succès", "model": UserCreateResponse},
        400: {"description": "Nom d'utilisateur ou email déjà utilisé", "model": UserError},
        422: {"description": "Validation échouée - données invalides", "model": UserError}
    }
)
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db)
) -> UserCreateResponse:
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()

    if existing_user:
        errors: List[Dict[str, str]] = []
        if existing_user.username == username:
            errors.append({"field": "username", "message": "Ce nom d'utilisateur est déjà utilisé"})
        if existing_user.email == email:
            errors.append({"field": "email", "message": "Cette adresse email est déjà utilisée"})

        error_response = UserError(
            code=status.HTTP_400_BAD_REQUEST,
            message="Le nom d'utilisateur ou l'email est déjà utilisé",
            errors=errors
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.dict()
        )

    password_hash = get_password_hash(password)

    profile_url = None
    if profile_picture:
        filename = f"{uuid.uuid4()}_{profile_picture.filename}"
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_picture.file, buffer)
        profile_url = f"/static/profile_pictures/{filename}"

    new_user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password_hash=password_hash,
        created_at=datetime.utcnow(),
        is_active=True,
        profile_picture_url=profile_url
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response_data = UserResponseData(
        user_id=new_user.id,
        username=new_user.username,
        profile_picture_url=new_user.profile_picture_url
    )

    return UserCreateResponse(
        code=status.HTTP_201_CREATED,
        message="Utilisateur créé avec succès",
        data=response_data
    )


@router.get(
    "/{user_id}",
    response_model=UserResponseData,
    summary="Récupérer les infos d'un utilisateur",
    description="Renvoie les informations d’un utilisateur à partir de son identifiant.",
    responses={
        200: {"description": "Données de l'utilisateur", "model": UserResponseData},
        404: {"description": "Utilisateur non trouvé", "model": UserError}
    }
)
def get_user(
    user_id: uuid.UUID = Path(..., description="Identifiant unique de l'utilisateur"),
    db: Session = Depends(get_db)
) -> UserResponseData:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserError(
                code=404,
                message="Utilisateur introuvable",
                errors=[{"field": "user_id", "message": "Aucun utilisateur trouvé avec cet ID"}]
            ).dict()
        )

    return UserResponseData(
        user_id=user.id,
        username=user.username,
        profile_picture_url=user.profile_picture_url
    )
