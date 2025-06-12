# auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict
from datetime import timedelta
from ..database import get_db
from ..models import AppUser
from ..schemas import UserCreate, User, Token
from ..auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from .crud import get_user_by_phone, create_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return create_user(db, user)

@router.options("/login")
def options_login():
    headers = {
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Credentials": "true",
    }
    logger.info("Handling OPTIONS request for /login")
    return JSONResponse(status_code=200, headers=headers)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login request received: username={form_data.username}")
    user = get_user_by_phone(db, phone=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning("Login failed: Incorrect phone number or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    logger.info(f"Login successful for user ID {user.id}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_current_user(current_user: AppUser = Depends(get_current_user)):
    return current_user