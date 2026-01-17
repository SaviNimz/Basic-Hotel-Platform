"""
This module defines the core domain models:
- Hotel: Represents a hotel property
- RoomType: Represents a room type within a hotel
- RateAdjustment: Represents date-specific rate adjustments for room types
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)  # Hotel name must be unique
    location = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship: one hotel has many room types
    room_types = relationship("RoomType", back_populates="hotel")


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)  
    base_rate = Column(Float, nullable=False) 

    # Relationships
    hotel = relationship("Hotel", back_populates="room_types")
    adjustments = relationship("RateAdjustment", back_populates="room_type")


class RateAdjustment(Base):
    __tablename__ = "rate_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    adjustment_amount = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False) 

    # Relationship: each adjustment belongs to one room type
    room_type = relationship("RoomType", back_populates="adjustments")
