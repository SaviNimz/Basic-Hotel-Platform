from datetime import date, timedelta
from app.services.rate_service import rate_service
from app.models.hotel import RoomType, RateAdjustment


def test_rate_logic_simple(db_session):
    # Setup data manually in DB
    room = RoomType(name="Standard", base_rate=100.0, hotel_id=999) # Constraint might fail on hotel_id FK
    # Need valid hotel first
    from app.models.hotel import Hotel
    hotel = Hotel(name="Test Hotel", location="Test Loc")
    db_session.add(hotel)
    db_session.flush()
    room.hotel_id = hotel.id
    db_session.add(room)
    db_session.flush()

    # Test Base
    res = rate_service.calculate_effective_rate(db_session, room.id)
    assert res["effective_rate"] == 100.0

    # Add Adjustment
    adj = RateAdjustment(room_type_id=room.id, adjustment_amount=20, effective_date=date.today(), reason="Test")
    db_session.add(adj)
    db_session.commit()

    # Test Adjusted
    res = rate_service.calculate_effective_rate(db_session, room.id)
    assert res["effective_rate"] == 120.0
