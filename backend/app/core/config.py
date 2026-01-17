from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Basic Hotel Platform"
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./hotel.db"
    
    # Auth
    SECRET_KEY: str = "supersecretkey" # In production, this should be overriden by env var
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
