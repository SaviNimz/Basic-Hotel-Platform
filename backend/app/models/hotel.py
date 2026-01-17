from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from app.models.base import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    location = Column(String)
    is_active = Column(Boolean, default=True)

    room_types = relationship("RoomType", back_populates="hotel")

class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    name = Column(String)
    base_rate = Column(Float)

    hotel = relationship("Hotel", back_populates="room_types")
    adjustments = relationship("RateAdjustment", back_populates="room_type")

class RateAdjustment(Base):
    __tablename__ = "rate_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"))
    adjustment_amount = Column(Float)
    effective_date = Column(Date)
    reason = Column(String)

    room_type = relationship("RoomType", back_populates="adjustments")
