# messages/routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import AppUser, DeliveryRequest
from ..schemas import MessageCreate, Message
from ..auth import get_current_user
from ..delivery.crud import get_delivery_request
from .crud import create_message, get_messages_by_delivery_request

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post("/", response_model=Message)
def create_message_endpoint(
    message: MessageCreate,
    delivery_request_id: int,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    return create_message(db, message, delivery_request_id=delivery_request_id, sender_id=current_user.id)

@router.get("/delivery-request/{delivery_request_id}", response_model=List[Message])
def get_messages_by_delivery_request_endpoint(
    delivery_request_id: int,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    db_request = get_delivery_request(db, request_id=delivery_request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Delivery request not found")
    if db_request.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_messages_by_delivery_request(db, delivery_request_id=delivery_request_id)