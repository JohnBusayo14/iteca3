# backend/main.py (temporary for direct testing)
from .core.app import app  
from backend.auth.routers import router as auth_router
from backend.delivery.routers import router as delivery_router
from backend.notifications.routers import router as notifications_router
from backend.messages.routers import router as messages_router
from backend.deliverer_applications.routers import router as deliverer_applications_router
from backend.deliverers.routers import router as deliverers_router

app.include_router(auth_router)
app.include_router(delivery_router)
app.include_router(notifications_router)
app.include_router(messages_router)
app.include_router(deliverer_applications_router)
app.include_router(deliverers_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Delivery API"}