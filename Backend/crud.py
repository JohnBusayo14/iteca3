# crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas
from utils import calculate_delivery_price

# User CRUD
def get_user_by_phone(db: Session, phone: str) -> Optional[models.AppUser]:
    return db.query(models.AppUser).filter(models.AppUser.phone == phone).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.AppUser:
    from auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.AppUser(
        name=user.name,
        phone=user.phone,
        email=user.email,
        role=user.role,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delivery Request CRUD
def create_delivery_request(db: Session, request: schemas.DeliveryRequestCreate, user_id: int) -> Optional[models.AppDeliveryRequest]:
    db_request = models.AppDeliveryRequest(
        user_id=user_id,
        parcel_name=request.parcel_name,
        recipient_name=request.recipient_name,
        recipient_mobile=request.recipient_mobile,
        recipient_email=request.recipient_email,
        pickup_lat=request.pickup_lat,
        pickup_lon=request.pickup_lon,
        dropoff_lat=request.dropoff_lat,
        dropoff_lon=request.dropoff_lon,
        note=request.note,
        send_code=request.send_code,
        weight=request.weight,
        state="Pending"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_delivery_requests(db: Session) -> List[models.AppDeliveryRequest]:
    return db.query(models.AppDeliveryRequest).all()

def get_user_delivery_requests(db: Session, user_id: int) -> List[models.AppDeliveryRequest]:
    return db.query(models.AppDeliveryRequest).filter(models.AppDeliveryRequest.user_id == user_id).all()

def get_delivery_request(db: Session, request_id: int) -> Optional[models.AppDeliveryRequest]:
    return db.query(models.AppDeliveryRequest).filter(models.AppDeliveryRequest.id == request_id).first()

def update_delivery_request(
    db: Session,
    request_id: int,
    state: Optional[str] = None,
    deliverer_id: Optional[int] = None
) -> Optional[models.AppDeliveryRequest]:
    db_request = db.query(models.AppDeliveryRequest).filter(models.AppDeliveryRequest.id == request_id).first()
    if not db_request:
        return None
    if state is not None:
        db_request.state = state
    if deliverer_id is not None:
        db_request.deliverer_id = deliverer_id
    db.commit()
    db.refresh(db_request)
    return db_request

# Notification CRUD
def create_notification(
    db: Session,
    notification: schemas.NotificationCreate,
    user_id: int,
    delivery_request_id: Optional[int] = None
) -> models.AppNotification:
    db_notification = models.AppNotification(
        user_id=user_id,
        message=notification.message,
        read=notification.read,
        delivery_request_id=delivery_request_id
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_user_notifications(db: Session, user_id: int) -> List[models.AppNotification]:
    return db.query(models.AppNotification).filter(models.AppNotification.user_id == user_id).all()

def update_notification(db: Session, notification_id: int, read: bool) -> Optional[models.AppNotification]:
    db_notification = db.query(models.AppNotification).filter(models.AppNotification.id == notification_id).first()
    if not db_notification:
        return None
    db_notification.read = read
    db.commit()
    db.refresh(db_notification)
    return db_notification

# Message CRUD
def create_message(
    db: Session,
    message: schemas.MessageCreate,
    delivery_request_id: int,
    sender_id: int
) -> models.AppMessage:
    db_message = models.AppMessage(
        delivery_request_id=delivery_request_id,
        sender_id=sender_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_delivery_request(db: Session, delivery_request_id: int) -> List[models.AppMessage]:
    return db.query(models.AppMessage).filter(models.AppMessage.delivery_request_id == delivery_request_id).all()

# Deliverer Application CRUD
def create_deliverer_application(
    db: Session,
    deliverer_application: schemas.DelivererApplicationCreate,
    user_id: int
) -> models.AppDelivererApplication:
    db_application = models.AppDelivererApplication(
        user_id=user_id,
        license_number=deliverer_application.license_number,
        vehicle_type=deliverer_application.vehicle_type
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_deliverer_applications(db: Session) -> List[models.AppDelivererApplication]:
    return db.query(models.AppDelivererApplication).all()

def update_deliverer_application(
    db: Session,
    application_id: int,
    status: str
) -> Optional[models.AppDelivererApplication]:
    db_application = db.query(models.AppDelivererApplication).filter(models.AppDelivererApplication.id == application_id).first()
    if not db_application:
        return None
    db_application.status = status
    db.commit()
    db.refresh(db_application)
    return db_application

# Deliverer CRUD
def create_deliverer(db: Session, deliverer: schemas.DelivererCreate, user_id: int) -> models.AppDeliverer:
    db_deliverer = models.AppDeliverer(
        user_id=user_id,
        name=deliverer.name,
        phone=deliverer.phone
    )
    db.add(db_deliverer)
    db.commit()
    db.refresh(db_deliverer)
    return db_deliverer

def get_deliverers(db: Session) -> List[models.AppDeliverer]:
    return db.query(models.AppDeliverer).all()