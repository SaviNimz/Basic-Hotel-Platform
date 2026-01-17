from app.database import SessionLocal, engine
from app.models import User, Base
from app.auth import get_password_hash

def seed_data():
    db = SessionLocal()
    # Check if user exists
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        print("Seeding admin user...")
        hashed_password = get_password_hash("password123")
        db_user = User(username="admin", password_hash=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print("Admin user seeded.")
    else:
        print("Admin user already exists.")
    
    db.close()

if __name__ == "__main__":
    seed_data()
