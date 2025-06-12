# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AppUser(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)
    role = Column(String, default="user", nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    delivery_requests = relationship("AppDeliveryRequest", back_populates="user")
    notifications = relationship("AppNotification", back_populates="user")
    messages = relationship("AppMessage", back_populates="sender")
    deliverer_applications = relationship("AppDelivererApplication", back_populates="user")
    deliverer = relationship("AppDeliverer", back_populates="user", uselist=False)

class AppDeliveryRequest(Base):
    __tablename__ = "delivery_requests"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    deliverer_id = Column(Integer, ForeignKey("deliverers.id", ondelete="SET NULL"), nullable=True)
    parcel_name = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_mobile = Column(String, nullable=False)
    recipient_email = Column(String, nullable=True)
    pickup_lat = Column(Float, nullable=False)
    pickup_lon = Column(Float, nullable=False)
    dropoff_lat = Column(Float, nullable=False)
    dropoff_lon = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    send_code = Column(Boolean, default=False, nullable=False)
    weight = Column(Float, nullable=False)
    state = Column(String, default="Pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("AppUser", back_populates="delivery_requests")
    deliverer = relationship("AppDeliverer", back_populates="delivery_requests")
    notifications = relationship("AppNotification", back_populates="delivery_request")
    messages = relationship("AppMessage", back_populates="delivery_request")

class AppNotification(Base):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivery_request_id = Column(Integer, ForeignKey("delivery_requests.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    user = relationship("AppUser", back_populates="notifications")
    delivery_request = relationship("AppDeliveryRequest", back_populates="notifications")

class AppMessage(Base):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    delivery_request_id = Column(Integer, ForeignKey("delivery_requests.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    delivery_request = relationship("AppDeliveryRequest", back_populates="messages")
    sender = relationship("AppUser", back_populates="messages")

class AppDelivererApplication(Base):
    __tablename__ = "deliverer_applications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    license_number = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False)
    status = Column(String, default="Pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("AppUser", back_populates="deliverer_applications")

class AppDeliverer(Base):
    __tablename__ = "deliverers"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # Relationships
    user = relationship("AppUser", back_populates="deliverer")
    delivery_requests = relationship("AppDeliveryRequest", back_populates="deliverer")