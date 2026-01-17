"""
User-related Pydantic schemas for request/response validation.

"""
from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    """
    Base user schema with common fields.
    """
    username: str

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    """
    username: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """
    User schema for API responses.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class UserLogin(BaseModel):
    """
    Schema for login credentials.
    """
    username: str
    password: str

class Token(BaseModel):
    """
    Schema for JWT access token response.
    """
    access_token: str
    token_type: str
