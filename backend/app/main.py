from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routers import api_router

# Initialize FastAPI application
app = FastAPI(
    title="Basic Hotel Platform",
    description="Internal hotel admin tool for managing hotels, room types, and rate adjustments",
    version="1.0.0"
)

# Configure CORS for frontend access
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS, 
        allow_credentials=True,  
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

app.include_router(api_router)
