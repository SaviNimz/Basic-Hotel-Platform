"""
This package exports all Pydantic models used for API validation and serialization.
"""
from .user import UserLogin, Token, User, UserCreate, UserUpdate
from .hotel import HotelBase, HotelCreate, HotelUpdate, Hotel
from .room import (
    RoomTypeBase,
    RoomTypeCreate,
    RoomTypeUpdate,
    RoomType,
    RateAdjustmentBase,
    RateAdjustmentCreate,
    RateAdjustmentUpdate,
    RateAdjustment,
)
