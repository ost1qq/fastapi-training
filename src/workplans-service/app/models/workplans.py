from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.database import Base

class WorkPlanModel(Base):
    __tablename__ = "work_plans"

    id: Mapped[int] = mapped_column(primary_key=True)

    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id"))
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"))