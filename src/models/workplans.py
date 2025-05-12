from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.brigades import BrigadeModel
    from models.requests import RequestModel

class WorkPlanModel(Base):
    __tablename__ = "work_plans"

    id: Mapped[int] = mapped_column(primary_key=True)

    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id"))
    brigade: Mapped["BrigadeModel"] = relationship(back_populates="work_plans")

    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"))
    request: Mapped["RequestModel"] = relationship(back_populates="work_plan")