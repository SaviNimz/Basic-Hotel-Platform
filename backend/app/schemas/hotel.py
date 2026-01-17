from pydantic import BaseModel
from typing import Optional

class HotelBase(BaseModel):
    name: str
    location: str
    is_active: bool = True

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: int
    class Config:
        from_attributes = True
