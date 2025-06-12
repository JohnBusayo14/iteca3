# deliverer_applications/crud.py
from sqlalchemy.orm import Session
from typing import List
from ..models import DelivererApplication
from ..schemas import DelivererApplicationCreate, DelivererApplication

def create_deliverer_application(db: Session, deliverer_application: DelivererApplicationCreate, user_id: int) -> DelivererApplication:
    db_application = DelivererApplication(**deliverer_application.dict(), user_id=user_id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_deliverer_applications(db: Session) -> List[DelivererApplication]:
    return db.query(DelivererApplication).all()

def update_deliverer_application(db: Session, application_id: int, status: str) -> DelivererApplication:
    db_application = db.query(DelivererApplication).filter(DelivererApplication.id == application_id).first()
    if not db_application:
        return None
    db_application.status = status
    db.commit()
    db.refresh(db_application)
    return db_application