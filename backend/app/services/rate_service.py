from datetime import date
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.hotel import RoomType, RateAdjustment

class RateService:
    @staticmethod
    def calculate_effective_rate(db: Session, room_type_id: int, target_date: date = None):
        if target_date is None:
            target_date = date.today()
        
        room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
        if not room_type:
            return None
            
        latest_adjustment = (
            db.query(RateAdjustment)
            .filter(
                RateAdjustment.room_type_id == room_type_id,
                RateAdjustment.effective_date <= target_date
            )
            .order_by(desc(RateAdjustment.effective_date))
            .first()
        )
        
        final_rate = room_type.base_rate
        adjustment_amount = 0.0
        if latest_adjustment:
            adjustment_amount = latest_adjustment.adjustment_amount
            final_rate += adjustment_amount
            
        return {
            "room_type_id": room_type.id,
            "base_rate": room_type.base_rate,
            "effective_rate": final_rate,
            "adjustment_applied": adjustment_amount,
            "effective_date": target_date
        }

rate_service = RateService()
