# deliverer_applications/routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import AppUser
from ..schemas import DelivererApplicationCreate, DelivererApplication, DelivererCreate
from ..auth import get_current_user
from ..core.dependencies import get_current_admin
from ..deliverers.crud import create_deliverer
from .crud import create_deliverer_application, get_deliverer_applications, update_deliverer_application
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/deliverer-applications",
    tags=["deliverer-applications"]
)

@router.post("/", response_model=DelivererApplication)
def create_deliverer_application_endpoint(
    deliverer_application: DelivererApplicationCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    return create_deliverer_application(db, deliverer_application, user_id=current_user.id)

@router.get("/", response_model=List[DelivererApplication])
def get_deliverer_applications_endpoint(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_admin)
):
    return get_deliverer_applications(db)

@router.patch("/{application_id}", response_model=DelivererApplication)
def update_deliverer_application_endpoint(
    application_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_admin)
):
    updated_application = update_deliverer_application(db, application_id=application_id, status=status)
    if not updated_application:
        raise HTTPException(status_code=404, detail="Deliverer application not found")
    if status == "Approved":
        create_deliverer(db, DelivererCreate(user_id=updated_application.user_id, name="", phone=""), user_id=updated_application.user_id)
    logger.info(f"Updated deliverer application {application_id}: status={status}")
    return updated_application