# delivery/crud.py
from sqlalchemy.orm import Session
from typing import List
from ..models import DeliveryRequest
from ..schemas import DeliveryRequestCreate, DeliveryRequest

def create_delivery_request(db: Session, request: DeliveryRequestCreate, user_id: int) -> DeliveryRequest:
    db_request = DeliveryRequest(user_id=user_id, **request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_delivery_requests(db: Session) -> List[DeliveryRequest]:
    return db.query(DeliveryRequest).all()

def get_user_delivery_requests(db: Session, user_id: int) -> List[DeliveryRequest]:
    return db.query(DeliveryRequest).filter(DeliveryRequest.user_id == user_id).all()

def get_delivery_request(db: Session, request_id: int) -> DeliveryRequest:
    return db.query(DeliveryRequest).filter(DeliveryRequest.id == request_id).first()

def update_delivery_request(db: Session, request_id: int, request_update: dict) -> DeliveryRequest:
    db_request = get_delivery_request(db, request_id)
    if not db_request:
        return None
    for key, value in request_update.items():
        setattr(db_request, key, value)
    db.commit()
    db.refresh(db_request)
    return db_request