from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, services
from app.api import deps

router = APIRouter()


@router.post("/hotels/", response_model=schemas.Hotel)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return services.hotel.create(db=db, obj_in=hotel)


@router.get("/hotels/", response_model=List[schemas.Hotel])
def read_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    hotels = services.hotel.get_multi(db, skip=skip, limit=limit)
    return hotels


@router.get("/hotels/{hotel_id}", response_model=schemas.Hotel)
def read_hotel(hotel_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_user)):
    db_hotel = services.hotel.get(db, id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel


@router.put("/hotels/{hotel_id}", response_model=schemas.Hotel)
def update_hotel(
    hotel_id: int,
    hotel_in: schemas.HotelUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_hotel = services.hotel.get(db, id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return services.hotel.update(db=db, db_obj=db_hotel, obj_in=hotel_in)


@router.delete("/hotels/{hotel_id}", response_model=schemas.Hotel)
def delete_hotel(
    hotel_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_hotel = services.hotel.remove(db, id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel
