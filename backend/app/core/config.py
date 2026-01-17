"""
This module uses Pydantic's BaseSettings to manage configuration values.
Settings can be overridden using environment variables defined in a .env file.

"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    All settings can be overridden via .env file or environment variables.
    """
    model_config = ConfigDict(case_sensitive=True, env_file=".env")
    
    PROJECT_NAME: str = "Basic Hotel Platform"
    
    # Database configuration
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./hotel.db"
    

    # This value is hardcoded only for the assignment
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173", 
        "http://localhost:3000",
        "http://frontend"  # Docker service name
    ]

# Global settings instance
settings = Settings()
