# backend/app/api/endpoints/event.py

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from datetime import datetime
from typing import List
import os
import shutil

from app.models import Event
from app.schemas import EventCreateResponse, EventResponseData
from app.database import get_db

router = APIRouter()

UPLOAD_BANNER_DIR = "app/static/event_banners"
os.makedirs(UPLOAD_BANNER_DIR, exist_ok=True)

@router.post(
    "/",
    response_model=EventCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un événement musical (avec bannière)",
    description="Création d'événement avec la possibilité d'ajouter une image de bannière.",
    tags=["Événements"]
)
async def create_event_with_banner(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    event_date: datetime = Form(...),
    tags: str = Form(""),
    banner: UploadFile = File(None),
    db: Session = Depends(get_db)
) -> EventCreateResponse:
    print("=== CRÉATION ÉVÉNEMENT AVEC BANNIÈRE ===")

    # ✅ ID simulé d'un utilisateur
    fake_user_id = UUID("002fb3d7-25e3-4d4a-b106-c70fe37427a0")

    banner_url = None
    if banner:
        filename = f"{uuid4()}_{banner.filename}"
        filepath = os.path.join(UPLOAD_BANNER_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(banner.file, buffer)
        banner_url = f"/static/event_banners/{filename}"

    new_event = Event(
        id=uuid4(),
        title=title,
        description=description,
        location=location,
        event_date=event_date,
        tags=tags.split(",") if tags else [],
        created_at=datetime.utcnow(),
        organizer_id=fake_user_id,
        banner_url=banner_url,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return EventCreateResponse(data=EventResponseData.model_validate(new_event))


@router.get(
    "/",
    response_model=List[EventResponseData],
    status_code=status.HTTP_200_OK,
    summary="Lister tous les événements",
    description="Récupère la liste de tous les événements disponibles.",
    tags=["Événements"]
)
def get_all_events(
    db: Session = Depends(get_db)
) -> List[EventResponseData]:
    events = db.query(Event).all()
    return [EventResponseData.model_validate(event) for event in events]


@router.get(
    "/{event_id}",
    response_model=EventResponseData,
    status_code=status.HTTP_200_OK,
    summary="Récupérer un événement par ID",
    description="Permet de récupérer les détails d’un événement en utilisant son identifiant unique.",
    tags=["Événements"]
)
def get_event_by_id(
    event_id: UUID,
    db: Session = Depends(get_db)
) -> EventResponseData:
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")

    return EventResponseData.model_validate(event)
