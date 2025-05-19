from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import Base

class BrigadeModel(Base):
    __tablename__ = "brigades"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    worker_count: Mapped[int]