# delivery/routers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import AppUser
from ..schemas import DeliveryRequestCreate, DeliveryRequest, EstimatePriceRequest
from ..auth import get_current_user
from ..core.dependencies import get_current_admin
from .crud import create_delivery_request, get_delivery_requests, get_user_delivery_requests, get_delivery_request, update_delivery_request
from .services import estimate_price
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/delivery",
    tags=["delivery"]
)

@router.post("/requests/", response_model=DeliveryRequest)
def create_delivery_request_endpoint(
    request: DeliveryRequestCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    return create_delivery_request(db, request, user_id=current_user.id)

@router.get("/requests/", response_model=List[DeliveryRequest])
def get_delivery_requests_endpoint(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_admin)
):
    return get_delivery_requests(db)

@router.get("/requests/my-requests", response_model=List[DeliveryRequest])
def get_my_delivery_requests(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    return get_user_delivery_requests(db, user_id=current_user.id)

@router.get("/requests/{request_id}", response_model=DeliveryRequest)
def get_delivery_request_endpoint(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    db_request = get_delivery_request(db, request_id=request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Delivery request not found")
    if db_request.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db_request

@router.patch("/requests/{request_id}", response_model=DeliveryRequest)
def update_delivery_request_endpoint(
    request_id: int,
    request: DeliveryRequestCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user)
):
    db_request = get_delivery_request(db, request_id=request_id)
    if not db_request:
        logger.error(f"Delivery request {request_id} not found")
        raise HTTPException(status_code=404, detail="Delivery request not found")
    if db_request.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_request = update_delivery_request(db, request_id, request.dict())
    logger.info(f"Updated delivery request {request_id}")
    return updated_request

@router.post("/estimate-price/", summary="Estimate delivery price")
async def estimate_price_endpoint(request: EstimatePriceRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Estimating price for request: pickup=({request.pickup_lat}, {request.pickup_lon}), dropoff=({request.dropoff_lat}, {request.dropoff_lon}), weight={request.weight}, send_code={request.send_code}")
        price = estimate_price(request)
        logger.info(f"Estimated price: {price}")
        return {"estimated_price": price}
    except Exception as e:
        logger.error(f"Error calculating price: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error calculating price: {str(e)}")