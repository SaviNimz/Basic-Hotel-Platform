from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class RoomTypeBase(BaseModel):
    name: str = Field(..., min_length=1)
    base_rate: float = Field(..., gt=0)
    hotel_id: int

class RoomTypeCreate(RoomTypeBase):
    pass

class RoomTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    base_rate: Optional[float] = Field(None, gt=0)
    hotel_id: Optional[int] = None

class RoomType(RoomTypeBase):
    id: int
    class Config:
        from_attributes = True

class RateAdjustmentBase(BaseModel):
    room_type_id: int
    adjustment_amount: float
    effective_date: date
    reason: str

class RateAdjustmentCreate(RateAdjustmentBase):
    pass

class RateAdjustmentUpdate(BaseModel):
    room_type_id: Optional[int] = None
    adjustment_amount: Optional[float] = None
    effective_date: Optional[date] = None
    reason: Optional[str] = None

class RateAdjustment(RateAdjustmentBase):
    id: int
    class Config:
        from_attributes = True
