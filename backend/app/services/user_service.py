from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.services.base import CRUDBase
from app.core.security import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_in_data = obj_in.model_dump()
        password = obj_in_data.pop("password")
        db_obj = User(username=obj_in_data["username"], password_hash=get_password_hash(password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        password = update_data.pop("password", None)
        if password:
            update_data["password_hash"] = get_password_hash(password)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

user = CRUDUser(User)
