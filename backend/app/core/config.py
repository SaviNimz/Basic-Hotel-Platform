from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True, env_file=".env")
    
    PROJECT_NAME: str = "Basic Hotel Platform"
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./hotel.db"
    
    # Auth
    SECRET_KEY: str = "supersecretkey" # In production, this should be overriden by env var
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

settings = Settings()
