from fastapi import APIRouter
from app.api.v1.routers import auth, users, hotels, rooms

# Main API router
api_router = APIRouter()

# sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(hotels.router, tags=["hotels"])
api_router.include_router(rooms.router, tags=["rooms"])
