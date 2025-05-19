from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from src.database import Base

class RequestModel(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    work_type: Mapped[str]
    scale: Mapped[str]
    preferred_time: Mapped[datetime]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))