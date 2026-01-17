"""
Hotel-related services for CRUD operations.
"""
from typing import List
from sqlalchemy.orm import Session
from app.models.hotel import Hotel, RoomType, RateAdjustment
from app.schemas.hotel import HotelCreate, HotelUpdate
from app.schemas.room import RoomTypeCreate, RoomTypeUpdate, RateAdjustmentCreate, RateAdjustmentUpdate
from app.services.base import CRUDBase


class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelUpdate]):
    """
    Hotel-specific CRUD operations.
    """
    pass


class CRUDRoomType(CRUDBase[RoomType, RoomTypeCreate, RoomTypeUpdate]):
    """
    Room Type-specific CRUD operations.
    """
    
    def get_by_hotel(self, db: Session, hotel_id: int) -> List[RoomType]:
        """
        Get all room types for a specific hotel.
        """
        return db.query(RoomType).filter(RoomType.hotel_id == hotel_id).all()


class CRUDRateAdjustment(CRUDBase[RateAdjustment, RateAdjustmentCreate, RateAdjustmentUpdate]):
    """
    Rate Adjustment-specific CRUD operations.
    """
    
    def get_by_room_type(self, db: Session, room_type_id: int) -> List[RateAdjustment]:
        """
        Get all rate adjustments for a specific room type.e
        """
        return db.query(RateAdjustment).filter(RateAdjustment.room_type_id == room_type_id).all()

# Service instances for dependency injection
hotel = CRUDHotel(Hotel)
room_type = CRUDRoomType(RoomType)
rate_adjustment = CRUDRateAdjustment(RateAdjustment)
