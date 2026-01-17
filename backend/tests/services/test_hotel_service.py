"""
Tests for hotel service operations.
"""
from app.services.hotel_service import hotel, room_type, rate_adjustment
from app.models.hotel import Hotel, RoomType, RateAdjustment
from app.schemas.hotel import HotelCreate, HotelUpdate
from app.schemas.room import RoomTypeCreate, RateAdjustmentCreate
from datetime import date


def test_create_hotel(db_session):
    """Test creating a new hotel."""
    hotel_in = HotelCreate(name="Test Hotel", location="Test City")
    created_hotel = hotel.create(db_session, obj_in=hotel_in)
    
    assert created_hotel.name == "Test Hotel"
    assert created_hotel.location == "Test City"
    assert created_hotel.is_active is True
    assert created_hotel.id is not None


def test_get_hotel(db_session):
    """Test retrieving a hotel by ID."""
    hotel_in = HotelCreate(name="Get Hotel", location="Get City")
    created = hotel.create(db_session, obj_in=hotel_in)
    
    retrieved = hotel.get(db_session, id=created.id)
    assert retrieved is not None
    assert retrieved.name == "Get Hotel"


def test_update_hotel(db_session):
    """Test updating hotel information."""
    hotel_in = HotelCreate(name="Old Name", location="Old Location")
    created = hotel.create(db_session, obj_in=hotel_in)
    
    update_data = HotelUpdate(name="New Name", location="New Location")
    updated = hotel.update(db_session, db_obj=created, obj_in=update_data)
    
    assert updated.name == "New Name"
    assert updated.location == "New Location"


def test_delete_hotel(db_session):
    """Test deleting a hotel."""
    hotel_in = HotelCreate(name="Delete Hotel", location="Delete City")
    created = hotel.create(db_session, obj_in=hotel_in)
    
    removed = hotel.remove(db_session, id=created.id)
    assert removed.id == created.id
    
    # Verify it's actually deleted
    retrieved = hotel.get(db_session, id=created.id)
    assert retrieved is None


def test_get_multi_hotels(db_session):
    """Test retrieving multiple hotels with pagination."""
    # Create multiple hotels
    for i in range(5):
        hotel_in = HotelCreate(name=f"Hotel {i}", location=f"City {i}")
        hotel.create(db_session, obj_in=hotel_in)
    
    hotels = hotel.get_multi(db_session, skip=0, limit=3)
    assert len(hotels) == 3


def test_room_type_get_by_hotel(db_session):
    """Test retrieving all room types for a specific hotel."""
    # Create a hotel
    hotel_in = HotelCreate(name="Room Type Hotel", location="RT City")
    h = hotel.create(db_session, obj_in=hotel_in)
    
    # Create multiple room types for this hotel
    for i in range(3):
        rt_in = RoomTypeCreate(name=f"Room Type {i}", base_rate=100.0 + i * 10, hotel_id=h.id)
        room_type.create(db_session, obj_in=rt_in)
    
    room_types = room_type.get_by_hotel(db_session, hotel_id=h.id)
    assert len(room_types) == 3


def test_rate_adjustment_get_by_room_type(db_session):
    """Test retrieving all rate adjustments for a specific room type."""
    # Create hotel and room type
    hotel_in = HotelCreate(name="Rate Hotel", location="Rate City")
    h = hotel.create(db_session, obj_in=hotel_in)
    
    rt_in = RoomTypeCreate(name="Rate Room", base_rate=100.0, hotel_id=h.id)
    rt = room_type.create(db_session, obj_in=rt_in)
    
    # Create multiple rate adjustments
    for i in range(3):
        adj_in = RateAdjustmentCreate(
            room_type_id=rt.id,
            adjustment_amount=10.0 + i * 5,
            effective_date=date.today(),
            reason=f"Adjustment {i}"
        )
        rate_adjustment.create(db_session, obj_in=adj_in)
    
    adjustments = rate_adjustment.get_by_room_type(db_session, room_type_id=rt.id)
    assert len(adjustments) == 3
