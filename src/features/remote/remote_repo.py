from fastapi.params import Depends
from sqlalchemy.orm import Session
from src.repositories.session import get_db
from .repository import Repository

class RemoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_repository(self, repo: Repository):
        try:
            existing_repo = self.db.query(Repository).filter(Repository.url == repo.url).first()
            if existing_repo:
                raise ValueError("Repository with this URL already exists")
            
            self.db.add(repo)
            self.db.commit()
            self.db.refresh(repo)
            return repo
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_repository(self, repo_id: int) -> Repository:
        return self.db.query(Repository).filter(Repository.id == repo_id).first()
    
    
    
def get_remote_repository(db: Session = Depends(get_db)) -> RemoteRepository:
    return RemoteRepository(db)