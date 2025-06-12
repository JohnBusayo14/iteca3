# auth/crud.py
from sqlalchemy.orm import Session
from ..models import AppUser
from ..schemas import UserCreate
from ..auth import get_password_hash

def get_user_by_phone(db: Session, phone: str) -> AppUser:
    return db.query(AppUser).filter(AppUser.phone == phone).first()

def create_user(db: Session, user: schemas.UserCreate) -> AppUser:
    hashed_password = get_password_hash(user.password)
    db_user = AppUser(
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