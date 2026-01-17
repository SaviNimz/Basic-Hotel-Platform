"""
Database seeding script for the Basic Hotel Platform.

This script seeds the database with an initial admin user for testing purposes.
The admin user credentials are:
- Username: admin
- Password: password123

Usage:
    python seed.py
"""
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def seed_data():
    """
    Seed the database with initial data.
    
    Creates an admin user if one doesn't already exist.
    The password is hashed before storing in the database.
    """
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        user = db.query(User).filter(User.username == "admin").first()
        
        if not user:
            print("Seeding admin user...")
            hashed_password = get_password_hash("password123")
            db_user = User(username="admin", password_hash=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            print("Admin user seeded successfully.")
            print("Username: admin")
            print("Password: password123")
        else:
            print("Admin user already exists.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
