"""
Tests for security module (password hashing and JWT tokens).
"""
from datetime import timedelta
import jwt
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token
)
from app.core.config import settings


def test_password_hash_and_verify():
    """Test password hashing and verification."""
    plain_password = "mysecretpassword"
    hashed = get_password_hash(plain_password)
    
    # Verify hash is different from plain text
    assert hashed != plain_password
    
    # Verify correct password
    assert verify_password(plain_password, hashed) is True
    
    # Verify incorrect password
    assert verify_password("wrongpassword", hashed) is False


def test_different_hashes_for_same_password():
    """Test that same password produces different hashes (salt is random)."""
    password = "testpassword"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different due to random salt
    assert hash1 != hash2
    
    # But both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_create_access_token():
    """Test JWT access token creation."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    # Verify token is a string
    assert isinstance(token, str)
    
    # Decode and verify token content
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded  # Expiration should be set


def test_create_access_token_with_expires_delta():
    """Test JWT token with custom expiration."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta=expires_delta)
    
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


def test_verify_empty_password():
    """Test that empty password verification works correctly."""
    hashed = get_password_hash("nonempty")
    assert verify_password("", hashed) is False


def test_verify_special_characters_password():
    """Test password with special characters."""
    special_password = "p@ssw0rd!#$%^&*()"
    hashed = get_password_hash(special_password)
    
    assert verify_password(special_password, hashed) is True
    assert verify_password("p@ssw0rd", hashed) is False
