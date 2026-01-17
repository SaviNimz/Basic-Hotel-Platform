"""
API dependencies for dependency injection.

This module provides FastAPI dependencies for:
- Database session management
- User authentication and authorization
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core import config
from app import services, models
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db() -> Generator:
    """
    Database session dependency.
    
    Yields a database session and ensures it's closed after use.
    Use in route functions with: db: Session = Depends(get_db)
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.User:
    """
    Get the current authenticated user from JWT token.
    
    This dependency extracts and validates the JWT token,
    then retrieves the corresponding user from the database.
    
    Args:
        token: JWT access token from Authorization header
        db: Database session
        
    Returns:
        The authenticated User instance
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            config.settings.SECRET_KEY, 
            algorithms=[config.settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Retrieve user from database
    user = services.user.get_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user
