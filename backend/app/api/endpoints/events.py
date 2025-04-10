from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from datetime import datetime
from typing import List

from app.models import Event
from app.schemas import EventCreate, EventCreateResponse, EventResponseData
from app.database import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=EventCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un événement musical (sans authentification)",
    description="Création d'événement ouverte pour tests sans login.",
    tags=["Événements"]
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
) -> EventCreateResponse:
    print("=== CRÉATION ÉVÉNEMENT SANS AUTH ===")

    # ✅ ID réel d'un utilisateur existant (extrait du token JWT de test)
    fake_user_id = UUID("50d5987d-c7a7-4633-8ec3-6871c8fcdd01")

    new_event = Event(
        id=uuid4(),
        title=event.title,
        description=event.description,
        location=event.location,
        event_date=event.event_date,
        tags=event.tags or [],
        created_at=datetime.utcnow(),
        organizer_id=fake_user_id,
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
    print("📥 Récupération de tous les événements...")
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
    print(f"🔍 Recherche de l'événement avec ID = {event_id}")
    
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")

    return EventResponseData.model_validate(event)
