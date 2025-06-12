# deliverers/routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import AppUser
from ..schemas import DelivererCreate, Deliverer
from ..auth import get_current_user
from ..core.dependencies import get_current_admin
from .crud import create_deliverer, get_deliverers

router = APIRouter(
    prefix="/deliverers",
    tags=["deliverers"]
)

@router.post("/", response_model=Deliverer)
def create_deliverer_endpoint(
    deliverer: DelivererCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_admin)
):
    return create_deliverer(db, deliverer, user_id=deliverer.user_id)

@router.get("/", response_model=List[Deliverer])
def get_deliverers_endpoint(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_admin)
):
    return get_deliverers(db)