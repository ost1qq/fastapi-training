from sqlalchemy import Column, Integer, String, Enum
from src.database import Base
import enum

class Role(str, enum.Enum):
    DISPATCHER = "DISPATCHER"
    HOUSEHOLDER = "HOUSEHOLDER"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
