"""
Tests for user service operations.
"""
import pytest
from app.services.user_service import user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password


def test_get_user_by_username(db_session):
    """Test retrieving a user by username."""
    # Create a test user
    user_in = UserCreate(username="testuser", password="testpass123")
    created_user = user.create(db_session, obj_in=user_in)
    
    # Retrieve the user by username
    retrieved_user = user.get_by_username(db_session, username="testuser")
    
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.id == created_user.id


def test_get_user_by_username_not_found(db_session):
    """Test retrieving a non-existent user returns None."""
    retrieved_user = user.get_by_username(db_session, username="nonexistent")
    assert retrieved_user is None


def test_create_user_hashes_password(db_session):
    """Test that password is properly hashed when creating a user."""
    user_in = UserCreate(username="hashtest", password="plainpassword")
    created_user = user.create(db_session, obj_in=user_in)
    
    # Verify password was hashed (not stored in plain text)
    assert created_user.password_hash != "plainpassword"
    # Verify the hash can be verified
    assert verify_password("plainpassword", created_user.password_hash)


def test_update_user_username(db_session):
    """Test updating a user's username."""
    # Create a user
    user_in = UserCreate(username="oldname", password="password123")
    created_user = user.create(db_session, obj_in=user_in)
    
    # Update username
    update_data = UserUpdate(username="newname")
    updated_user = user.update(db_session, db_obj=created_user, obj_in=update_data)
    
    assert updated_user.username == "newname"


def test_update_user_password(db_session):
    """Test updating a user's password rehashes it."""
    # Create a user
    user_in = UserCreate(username="passuser", password="oldpass")
    created_user = user.create(db_session, obj_in=user_in)
    old_hash = created_user.password_hash
    
    # Update password
    update_data = UserUpdate(password="newpass")
    updated_user = user.update(db_session, db_obj=created_user, obj_in=update_data)
    
    # Verify password was rehashed
    assert updated_user.password_hash != old_hash
    assert verify_password("newpass", updated_user.password_hash)
    assert not verify_password("oldpass", updated_user.password_hash)


def test_get_multi_users(db_session):
    """Test retrieving multiple users with pagination."""
    # Create multiple users
    for i in range(5):
        user_in = UserCreate(username=f"user{i}", password="password123")
        user.create(db_session, obj_in=user_in)
    
    # Get with default pagination
    users = user.get_multi(db_session, skip=0, limit=3)
    assert len(users) == 3
    
    # Get with offset
    users_offset = user.get_multi(db_session, skip=3, limit=3)
    assert len(users_offset) >= 2  # At least 2 more users (plus admin from conftest)
