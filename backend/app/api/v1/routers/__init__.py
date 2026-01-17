from fastapi import APIRouter
from app.api.v1.routers import auth, users, hotels, rooms

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(hotels.router, tags=["hotels"])
api_router.include_router(rooms.router, tags=["rooms"])
