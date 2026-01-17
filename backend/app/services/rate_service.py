"""
Rate calculation service for computing effective rates.

Implements the rate calculation algorithm as per requirements:
    effective_rate = base_rate + adjustment_amount

Where adjustment_amount is from the most recent RateAdjustment
with effective_date <= target_date.
"""
from datetime import date
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.hotel import RoomType, RateAdjustment


class RateService:
    """
    Service for calculating effective room rates based on adjustments.
    """
    
    @staticmethod
    def calculate_effective_rate(db: Session, room_type_id: int, target_date: date = None):
        """
        Calculate the effective rate for a room type on a specific date.
        """
        if target_date is None:
            target_date = date.today()
        
        # Get the room type
        room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
        if not room_type:
            return None
        
        # Find the most recent adjustment with effective_date <= target_date
        # Ordered by effective_date descending to get the latest applicable adjustment
        latest_adjustment = (
            db.query(RateAdjustment)
            .filter(
                RateAdjustment.room_type_id == room_type_id,
                RateAdjustment.effective_date <= target_date
            )
            .order_by(desc(RateAdjustment.effective_date))
            .first()
        )
        
        # Calculate effective rate using the formula: base_rate + adjustment_amount
        final_rate = room_type.base_rate
        adjustment_amount = 0.0
        if latest_adjustment:
            adjustment_amount = latest_adjustment.adjustment_amount
            final_rate += adjustment_amount
        
        # Return detailed rate calculation information
        return {
            "room_type_id": room_type.id,
            "base_rate": room_type.base_rate,
            "effective_rate": final_rate,
            "adjustment_applied": adjustment_amount,
            "effective_date": target_date
        }


# Service instance for dependency injection
rate_service = RateService()
