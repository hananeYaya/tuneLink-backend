from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.message import Message
from app.schemas.message import (
    MessageCreate,
    MessageData,
    MessageResponse,
    MessageListResponse,
    MessageDeleteResponse
)

router = APIRouter()

@router.post(
    "/messages",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    summary="Envoyer un message",
    description="Envoie un message à un autre utilisateur."
)
async def send_message(message: MessageCreate, db: Session = Depends(get_db)) -> MessageResponse:
    new_message = Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content,
        timestamp=datetime.utcnow()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return MessageResponse(
        code=status.HTTP_201_CREATED,
        message="Message envoyé avec succès",
        data=new_message
    )


@router.get(
    "/messages/{user1_id}/{user2_id}",
    response_model=MessageListResponse,
    summary="Récupérer les messages entre deux utilisateurs",
    description="Retourne tous les messages échangés entre deux utilisateurs."
)
async def get_messages(user1_id: UUID, user2_id: UUID, db: Session = Depends(get_db)) -> MessageListResponse:
    messages = db.query(Message).filter(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
        ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    ).order_by(Message.timestamp.asc()).all()

    return MessageListResponse(
        code=status.HTTP_200_OK,
        message="Messages récupérés avec succès",
        data=messages
    )


@router.delete(
    "/messages/{message_id}",
    response_model=MessageDeleteResponse,
    summary="Supprimer un message",
    description="Supprime un message par son ID."
)
async def delete_message(message_id: UUID, db: Session = Depends(get_db)) -> MessageDeleteResponse:
    message = db.query(Message).get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message introuvable")

    db.delete(message)
    db.commit()

    return MessageDeleteResponse(
        code=status.HTTP_200_OK,
        message="Message supprimé avec succès"
    )
