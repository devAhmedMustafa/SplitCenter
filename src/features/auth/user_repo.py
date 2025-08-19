from fastapi.params import Depends
from sqlalchemy.orm import Session
from .user import User
from repositories.session import get_db

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, email: str) -> User:
        user = User(email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)