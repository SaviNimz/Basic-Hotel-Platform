from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserLogin
from app.services.base import CRUDBase, CreateSchemaType, UpdateSchemaType

class CRUDUser(CRUDBase[User, UserLogin, UserLogin]): # Using UserLogin as placeholder for Create/Update schemas if specific ones don't exist
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

user = CRUDUser(User)
