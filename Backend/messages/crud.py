# messages/crud.py
from sqlalchemy.orm import Session
from typing import List
from ..models import Message
from ..schemas import MessageCreate, Message

def create_message(db: Session, message: MessageCreate, delivery_request_id: int, sender_id: int) -> Message:
    db_message = Message(**message.dict(), delivery_request_id=delivery_request_id, sender_id=sender_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_delivery_request(db: Session, delivery_request_id: int) -> List[Message]:
    return db.query(Message).filter(Message.delivery_request_id == delivery_request_id).all()