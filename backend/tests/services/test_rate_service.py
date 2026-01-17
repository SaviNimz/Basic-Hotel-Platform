from datetime import date, timedelta
from app.services.rate_service import rate_service
from app.models.hotel import RoomType, RateAdjustment, Hotel

def test_rate_logic_simple(db_session):
    # Setup data
    hotel = Hotel(name="Test Hotel", location="Test Loc")
    db_session.add(hotel)
    db_session.flush()
    
    room = RoomType(name="Standard", base_rate=100.0, hotel_id=hotel.id)
    db_session.add(room)
    db_session.flush()

    # Test Base
    res = rate_service.calculate_effective_rate(db_session, room.id)
    assert res["effective_rate"] == 100.0

    # Add Adjustment Today
    adj = RateAdjustment(room_type_id=room.id, adjustment_amount=20, effective_date=date.today(), reason="Test")
    db_session.add(adj)
    db_session.commit()

    # Test Adjusted
    res = rate_service.calculate_effective_rate(db_session, room.id)
    assert res["effective_rate"] == 120.0

def test_future_adjustment(db_session):
    # Setup data
    hotel = Hotel(name="Future Hotel", location="Loc")
    db_session.add(hotel)
    db_session.flush()
    room = RoomType(name="Future Room", base_rate=100.0, hotel_id=hotel.id)
    db_session.add(room)
    db_session.flush()

    # Add Future Adjustment
    future_date = date.today() + timedelta(days=10)
    adj = RateAdjustment(room_type_id=room.id, adjustment_amount=50, effective_date=future_date, reason="Future")
    db_session.add(adj)
    db_session.commit()

    # Check logic with today (should ignore future)
    res = rate_service.calculate_effective_rate(db_session, room.id)
    assert res["effective_rate"] == 100.0

    # Check logic with future date
    res_future = rate_service.calculate_effective_rate(db_session, room.id, target_date=future_date)
    assert res_future["effective_rate"] == 150.0

def test_multiple_adjustments(db_session):
    # Setup data
    hotel = Hotel(name="Multi Hotel", location="Loc")
    db_session.add(hotel)
    db_session.flush()
    room = RoomType(name="Multi Room", base_rate=100.0, hotel_id=hotel.id)
    db_session.add(room)
    db_session.flush()

    # Old adjustment
    adj1 = RateAdjustment(room_type_id=room.id, adjustment_amount=10, effective_date=date.today() - timedelta(days=5), reason="Old")
    db_session.add(adj1)
    
    # Newer adjustment (but still valid)
    adj2 = RateAdjustment(room_type_id=room.id, adjustment_amount=30, effective_date=date.today(), reason="New")
    db_session.add(adj2)
    db_session.commit()

    # Should pick the latest effective one (adj2)
    res = rate_service.calculate_effective_rate(db_session, room.id)
    assert res["effective_rate"] == 130.0
