# schemas.py
from pydantic import BaseModel, computed_field
from typing import Optional
from datetime import datetime
from utils import calculate_delivery_price

# User Schemas
class UserBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    role: str = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Delivery Request Schemas
class DeliveryRequestBase(BaseModel):
    parcel_name: str
    recipient_name: str
    recipient_mobile: str
    recipient_email: Optional[str] = None
    pickup_lat: float
    pickup_lon: float
    dropoff_lat: float
    dropoff_lon: float
    note: Optional[str] = None
    send_code: bool = False
    weight: float

class DeliveryRequestCreate(DeliveryRequestBase):
    pass

class DeliveryRequest(DeliveryRequestBase):
    id: int
    user_id: int
    state: str
    created_at: datetime
    updated_at: datetime
    deliverer_id: Optional[int] = None

    @computed_field
    def price(self) -> float:
        return calculate_delivery_price(
            pickup_lat=self.pickup_lat,
            pickup_lon=self.pickup_lon,
            dropoff_lat=self.dropoff_lat,
            dropoff_lon=self.dropoff_lon,
            weight=self.weight,
            send_code=self.send_code
        )

    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    message: str
    read: bool = False

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime
    delivery_request_id: Optional[int] = None

    class Config:
        from_attributes = True

# Message Schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    delivery_request_id: int
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Deliverer Application Schemas
class DelivererApplicationBase(BaseModel):
    license_number: str
    vehicle_type: str

class DelivererApplicationCreate(DelivererApplicationBase):
    pass

class DelivererApplication(DelivererApplicationBase):
    id: int
    user_id: int
    status: str = "Pending"
    created_at: datetime

    class Config:
        from_attributes = True

# Deliverer Schemas
class DelivererBase(BaseModel):
    name: str
    phone: str

class DelivererCreate(DelivererBase):
    pass

class Deliverer(DelivererBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Estimate Price Schema
class EstimatePriceRequest(BaseModel):
    pickup_lat: float
    pickup_lon: float
    dropoff_lat: float
    dropoff_lon: float
    weight: float
    send_code: bool = False