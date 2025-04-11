from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.user import User
from app.schemas.auth import Token
from app.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.exceptions import APIException
from app.config import settings

router = APIRouter()

@router.post(
    "/login",
    response_model=Token,
    summary="Authentifier un utilisateur",
    description="Authentifie un utilisateur avec son email et son mot de passe, puis retourne un token JWT."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    user = db.query(User).filter(
        (User.email == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Identifiants incorrects",
            errors=[{"field": "credentials", "message": "Email ou mot de passe incorrect"}]
        )

    if not user.is_active:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Utilisateur inactif",
            errors=[{"field": "user", "message": "Ce compte utilisateur est désactivé"}]
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token)
