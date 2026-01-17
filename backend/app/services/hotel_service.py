from typing import List
from sqlalchemy.orm import Session
from app.models.hotel import Hotel, RoomType, RateAdjustment
from app.schemas.hotel import HotelCreate, Hotel as HotelSchema
from app.schemas.room import RoomTypeCreate, RateAdjustmentCreate
from app.services.base import CRUDBase

class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelCreate]):
    pass

class CRUDRoomType(CRUDBase[RoomType, RoomTypeCreate, RoomTypeCreate]):
    def get_by_hotel(self, db: Session, hotel_id: int) -> List[RoomType]:
        return db.query(RoomType).filter(RoomType.hotel_id == hotel_id).all()

class CRUDRateAdjustment(CRUDBase[RateAdjustment, RateAdjustmentCreate, RateAdjustmentCreate]):
    pass

hotel = CRUDHotel(Hotel)
room_type = CRUDRoomType(RoomType)
rate_adjustment = CRUDRateAdjustment(RateAdjustment)
