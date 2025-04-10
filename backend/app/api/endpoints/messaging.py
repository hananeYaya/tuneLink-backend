from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

from app.database import get_db
from app.models import Conversation, ConversationParticipant, Message
from app.schemas.conversation import ConversationCreate, ConversationResponseData
from app.schemas.message import MessageCreate, MessageResponseData

router = APIRouter()


@router.post("/conversations", response_model=ConversationResponseData, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    new_conversation = Conversation(
        id=uuid4(),
        name=conversation.name,
        type=conversation.type,
        created_at=datetime.utcnow()
    )
    db.add(new_conversation)

    for participant_id in conversation.participant_ids:
        participant = ConversationParticipant(
            user_id=participant_id,
            conversation_id=new_conversation.id
        )
        db.add(participant)

    db.commit()
    db.refresh(new_conversation)

    return ConversationResponseData.model_validate(new_conversation)


@router.get("/conversations", response_model=List[ConversationResponseData])
def list_conversations(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).all()
    return [ConversationResponseData.model_validate(conv) for conv in conversations]


@router.post("/conversations", response_model=ConversationResponseData, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    new_conversation = Conversation(
        id=uuid4(),
        created_at=datetime.utcnow()
    )
    db.add(new_conversation)
    db.flush()  # pour obtenir l'ID généré

    for participant_id in conversation.participant_ids:
        participant = ConversationParticipant(
            user_id=participant_id,
            conversation_id=new_conversation.id
        )
        db.add(participant)

    db.commit()
    db.refresh(new_conversation)

    return ConversationResponseData.model_validate(new_conversation)


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponseData])
def get_messages_in_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
    return [MessageResponseData.model_validate(msg) for msg in messages]
