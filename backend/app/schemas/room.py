from pydantic import BaseModel
from datetime import date

class RoomTypeBase(BaseModel):
    name: str
    base_rate: float
    hotel_id: int

class RoomTypeCreate(RoomTypeBase):
    pass

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

class RateAdjustment(RateAdjustmentBase):
    id: int
    class Config:
        from_attributes = True
