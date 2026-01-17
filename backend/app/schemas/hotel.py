from pydantic import BaseModel, Field
from typing import Optional

class HotelBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the hotel")
    location: str = Field(..., min_length=1, description="Location of the hotel")
    is_active: bool = True

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: int
    class Config:
        from_attributes = True
