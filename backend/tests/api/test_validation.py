import pytest
from pydantic import ValidationError
from app.schemas.room import RoomTypeBase
from app.schemas.hotel import HotelBase


def test_room_validation():
    # Negative rate
    with pytest.raises(ValidationError):
        RoomTypeBase(name="Valid", base_rate=-10, hotel_id=1)
    
    # Check 0 rate (gt=0 means > 0)
    with pytest.raises(ValidationError):
        RoomTypeBase(name="Valid", base_rate=0, hotel_id=1)

    # Empty name
    with pytest.raises(ValidationError):
        RoomTypeBase(name="", base_rate=10, hotel_id=1)

    # Valid
    room = RoomTypeBase(name="Valid", base_rate=100, hotel_id=1)
    assert room.base_rate == 100


def test_hotel_validation():
    # Empty name
    with pytest.raises(ValidationError):
        HotelBase(name="", location="Loc")
    
    # Empty location
    with pytest.raises(ValidationError):
        HotelBase(name="Valid", location="")
    
    # Valid
    hotel = HotelBase(name="Valid", location="Loc")
    assert hotel.name == "Valid"
