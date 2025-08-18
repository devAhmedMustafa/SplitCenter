from sqlalchemy import Column, UUID, String, Boolean
from models.base import Base
import uuid

class User(Base):
    __tablename__ = "User"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4())
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
