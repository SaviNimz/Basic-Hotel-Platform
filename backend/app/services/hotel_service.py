from typing import List
from sqlalchemy.orm import Session
from app.models.hotel import Hotel, RoomType, RateAdjustment
from app.schemas.hotel import HotelCreate, HotelUpdate
from app.schemas.room import RoomTypeCreate, RoomTypeUpdate, RateAdjustmentCreate, RateAdjustmentUpdate
from app.services.base import CRUDBase

class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelUpdate]):
    pass

class CRUDRoomType(CRUDBase[RoomType, RoomTypeCreate, RoomTypeUpdate]):
    def get_by_hotel(self, db: Session, hotel_id: int) -> List[RoomType]:
        return db.query(RoomType).filter(RoomType.hotel_id == hotel_id).all()

class CRUDRateAdjustment(CRUDBase[RateAdjustment, RateAdjustmentCreate, RateAdjustmentUpdate]):
    def get_by_room_type(self, db: Session, room_type_id: int) -> List[RateAdjustment]:
        return db.query(RateAdjustment).filter(RateAdjustment.room_type_id == room_type_id).all()

hotel = CRUDHotel(Hotel)
room_type = CRUDRoomType(RoomType)
rate_adjustment = CRUDRateAdjustment(RateAdjustment)
