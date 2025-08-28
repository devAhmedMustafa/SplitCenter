from src.models.base import Base
from sqlalchemy import Column, String, Boolean, UUID, ForeignKey
import uuid

class Repository(Base):
    __tablename__ = "Repository"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4())
    url = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    owner = Column(UUID, ForeignKey("User.id"))
    is_active = Column(Boolean, default=True)