"""
Room type and rate adjustment schemas for request/response validation.
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional


class RoomTypeBase(BaseModel):
    """
    Base room type schema with validation.
    """
    name: str = Field(..., min_length=1, description="Room type name")
    base_rate: float = Field(..., gt=0, description="Base nightly rate, must be positive")
    hotel_id: int = Field(..., description="ID of the hotel this room type belongs to")


class RoomTypeCreate(RoomTypeBase):
    """
    Schema for creating a new room type.
    """
    pass


class RoomTypeUpdate(BaseModel):
    """
    Schema for updating room type information.
    """
    name: Optional[str] = Field(None, min_length=1)
    base_rate: Optional[float] = Field(None, gt=0)
    hotel_id: Optional[int] = None


class RoomType(RoomTypeBase):
    """
    Room type schema for API responses.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class RateAdjustmentBase(BaseModel):
    """
    Base rate adjustment schema with validation.
    """
    room_type_id: int = Field(..., description="ID of the room type")
    adjustment_amount: float = Field(..., description="Amount to adjust (positive or negative)")
    effective_date: date = Field(..., description="Date when this adjustment takes effect")
    reason: str = Field(..., min_length=1, description="Business reason for the adjustment")


class RateAdjustmentCreate(RateAdjustmentBase):
    """
    Schema for creating a new rate adjustment.
    """
    pass


class RateAdjustmentUpdate(BaseModel):
    """
    Schema for updating rate adjustment information.
    """
    room_type_id: Optional[int] = None
    adjustment_amount: Optional[float] = None
    effective_date: Optional[date] = None
    reason: Optional[str] = Field(None, min_length=1)


class RateAdjustment(RateAdjustmentBase):
    """
    Rate adjustment schema for API responses.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
