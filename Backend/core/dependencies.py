# core/dependencies.py
from fastapi import Depends, HTTPException, status
from .. import models
from ..auth import get_current_user

async def get_current_admin(current_user: models.AppUser = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user