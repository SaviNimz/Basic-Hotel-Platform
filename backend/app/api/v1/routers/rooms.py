from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, services
from app.api import deps

router = APIRouter()

# RoomType CRUD
@router.post("/room-types/", response_model=schemas.RoomType)
def create_room_type(room_type: schemas.RoomTypeCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return services.room_type.create(db=db, obj_in=room_type)

@router.get("/hotels/{hotel_id}/room-types/", response_model=List[schemas.RoomType])
def read_room_types(hotel_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return services.room_type.get_by_hotel(db, hotel_id=hotel_id)

# Rate Adjustment CRUD
@router.post("/rate-adjustments/", response_model=schemas.RateAdjustment)
def create_rate_adjustment(adjustment: schemas.RateAdjustmentCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    # Verify room type exists
    room_type_obj = services.room_type.get(db, id=adjustment.room_type_id)
    if not room_type_obj:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return services.rate_adjustment.create(db=db, obj_in=adjustment)

# Effective Rate
@router.get("/room-types/{room_type_id}/effective-rate")
def get_effective_rate(room_type_id: int, date_str: str = None, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    target_date = date.today()
    if date_str:
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format. Use YYYY-MM-DD")
            
    result = services.rate_service.calculate_effective_rate(db, room_type_id, target_date)
    if not result:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return result
