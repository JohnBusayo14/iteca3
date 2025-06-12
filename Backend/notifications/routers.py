# notifications/routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import AppUser
from ..schemas import NotificationCreate, Notification
from ..auth import get_current_user
from .crud import create_notification, get_user_notifications, update_notification
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.post("/", response_model=Notification)
def create_notification_endpoint(
    notification: NotificationCreate,
    delivery_request_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    return create_notification(db, notification, user_id=current_user.id, delivery_request_id=delivery_request_id)

@router.get("/", response_model=List[Notification])
def get_user_notifications_endpoint(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    return get_user_notifications(db, user_id=current_user.id)

@router.get("/user/{user_id}", response_model=List[Notification])
def get_user_notifications_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_user_notifications(db, user_id=user_id)

@router.patch("/{notification_id}", response_model=Notification)
def update_notification_endpoint(
    notification_id: int,
    read: bool,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    db_notification = update_notification(db, notification_id=notification_id, read=read)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if db_notification.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    logger.info(f"Updated notification {notification_id}: read={read}")
    return db_notification