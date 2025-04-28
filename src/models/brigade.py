from sqlalchemy import Column, Integer, String
from src.database import Base

class BrigadeModel(Base):
    __tablename__ = "brigades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
