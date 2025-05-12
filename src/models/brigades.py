from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import WorkPlanModel

class BrigadeModel(Base):
    __tablename__ = "brigades"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    worker_count: Mapped[int]

    work_plans: Mapped[list["WorkPlanModel"]] = relationship(back_populates="brigade")
