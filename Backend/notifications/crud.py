# notifications/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import Notification
from ..schemas import NotificationCreate, Notification

def create_notification(db: Session, notification: NotificationCreate, user_id: int, delivery_request_id: Optional[int] = None) -> Notification:
    db_notification = Notification(**notification.dict(), user_id=user_id, delivery_request_id=delivery_request_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_user_notifications(db: Session, user_id: int) -> List[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).all()

def update_notification(db: Session, notification_id: int, read: bool) -> Notification:
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not db_notification:
        return None
    db_notification.read = read
    db.commit()
    db.refresh(db_notification)
    return db_notification