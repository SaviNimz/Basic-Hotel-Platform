from fastapi import APIRouter, Depends
from app import models
from app.api import deps

router = APIRouter()

@router.get("/users/me")
async def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return {"username": current_user.username, "id": current_user.id}
