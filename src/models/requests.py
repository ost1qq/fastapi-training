from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import UserModel
    from src.models import WorkPlanModel

class RequestModel(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    work_type: Mapped[str]
    scale: Mapped[str]
    preferred_time: Mapped[datetime]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="requests")

    work_plan: Mapped["WorkPlanModel"] = relationship(back_populates="request", uselist=False)
