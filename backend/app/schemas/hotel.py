"""
Hotel-related Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class HotelBase(BaseModel):
    """
    Base hotel schema with common validation rules.
    """
    name: str = Field(..., min_length=1, description="Name of the hotel")
    location: str = Field(..., min_length=1, description="Location of the hotel")
    is_active: bool = True

class HotelCreate(HotelBase):
    """
    Schema for creating a new hotel.
    """
    pass

class HotelUpdate(BaseModel):
    """
    Schema for updating hotel information.
    
    """
    name: Optional[str] = Field(None, min_length=1, description="Name of the hotel")
    location: Optional[str] = Field(None, min_length=1, description="Location of the hotel")
    is_active: Optional[bool] = None

class Hotel(HotelBase):
    """
    Hotel schema for API responses.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
