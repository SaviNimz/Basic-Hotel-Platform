from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, services
from app.api import deps

router = APIRouter()


@router.post("/room-types/", response_model=schemas.RoomType)
def create_room_type(room_type: schemas.RoomTypeCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return services.room_type.create(db=db, obj_in=room_type)


@router.get("/hotels/{hotel_id}/room-types/", response_model=List[schemas.RoomType])
def read_room_types(hotel_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return services.room_type.get_by_hotel(db, hotel_id=hotel_id)


@router.get("/room-types/{room_type_id}", response_model=schemas.RoomType)
def read_room_type(
    room_type_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_room_type = services.room_type.get(db, id=room_type_id)
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return db_room_type


@router.put("/room-types/{room_type_id}", response_model=schemas.RoomType)
def update_room_type(
    room_type_id: int,
    room_type_in: schemas.RoomTypeUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_room_type = services.room_type.get(db, id=room_type_id)
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room Type not found")
    if room_type_in.hotel_id is not None:
        hotel = services.hotel.get(db, id=room_type_in.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return services.room_type.update(db=db, db_obj=db_room_type, obj_in=room_type_in)


@router.delete("/room-types/{room_type_id}", response_model=schemas.RoomType)
def delete_room_type(
    room_type_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_room_type = services.room_type.remove(db, id=room_type_id)
    if not db_room_type:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return db_room_type


@router.post("/rate-adjustments/", response_model=schemas.RateAdjustment)
def create_rate_adjustment(adjustment: schemas.RateAdjustmentCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    room_type_obj = services.room_type.get(db, id=adjustment.room_type_id)
    if not room_type_obj:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return services.rate_adjustment.create(db=db, obj_in=adjustment)


@router.get("/rate-adjustments/{adjustment_id}", response_model=schemas.RateAdjustment)
def read_rate_adjustment(
    adjustment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_adjustment = services.rate_adjustment.get(db, id=adjustment_id)
    if not db_adjustment:
        raise HTTPException(status_code=404, detail="Rate Adjustment not found")
    return db_adjustment


@router.get("/room-types/{room_type_id}/rate-adjustments/", response_model=List[schemas.RateAdjustment])
def read_rate_adjustments(
    room_type_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    room_type_obj = services.room_type.get(db, id=room_type_id)
    if not room_type_obj:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return services.rate_adjustment.get_by_room_type(db, room_type_id=room_type_id)


@router.put("/rate-adjustments/{adjustment_id}", response_model=schemas.RateAdjustment)
def update_rate_adjustment(
    adjustment_id: int,
    adjustment_in: schemas.RateAdjustmentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_adjustment = services.rate_adjustment.get(db, id=adjustment_id)
    if not db_adjustment:
        raise HTTPException(status_code=404, detail="Rate Adjustment not found")
    if adjustment_in.room_type_id is not None:
        room_type_obj = services.room_type.get(db, id=adjustment_in.room_type_id)
        if not room_type_obj:
            raise HTTPException(status_code=404, detail="Room Type not found")
    return services.rate_adjustment.update(db=db, db_obj=db_adjustment, obj_in=adjustment_in)


@router.delete("/rate-adjustments/{adjustment_id}", response_model=schemas.RateAdjustment)
def delete_rate_adjustment(
    adjustment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_adjustment = services.rate_adjustment.remove(db, id=adjustment_id)
    if not db_adjustment:
        raise HTTPException(status_code=404, detail="Rate Adjustment not found")
    return db_adjustment


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
