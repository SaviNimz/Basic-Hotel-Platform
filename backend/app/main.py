from fastapi import FastAPI
from app.api.v1.routers import api_router
from app.core import database

# Create tables
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Basic Hotel Platform")

app.include_router(api_router)
