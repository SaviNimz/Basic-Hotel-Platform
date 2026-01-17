from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas, services
from app.api import deps

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return {"username": current_user.username, "id": current_user.id}

@router.post("/", response_model=schemas.User)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    existing_user = services.user.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return services.user.create(db=db, obj_in=user_in)

@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    return services.user.get_multi(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_user = services.user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_user = services.user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.username:
        existing_user = services.user.get_by_username(db, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Username already registered")
    return services.user.update(db=db, db_obj=db_user, obj_in=user_in)

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    db_user = services.user.remove(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
