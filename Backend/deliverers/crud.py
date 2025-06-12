# deliverers/crud.py
from sqlalchemy.orm import Session
from typing import List
from ..models import Deliverer
from ..schemas import DelivererCreate, Deliverer

def create_deliverer(db: Session, deliverer: DelivererCreate, user_id: int) -> Deliverer:
    db_deliverer = Deliverer(**deliverer.dict(), user_id=user_id)
    db.add(db_deliverer)
    db.commit()
    db.refresh(db_deliverer)
    return db_deliverer

def get_deliverers(db: Session) -> List[Deliverer]:
    return db.query(Deliverer).all()