from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class HotelBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the hotel")
    location: str = Field(..., min_length=1, description="Location of the hotel")
    is_active: bool = True

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Name of the hotel")
    location: Optional[str] = Field(None, min_length=1, description="Location of the hotel")
    is_active: Optional[bool] = None

class Hotel(HotelBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
