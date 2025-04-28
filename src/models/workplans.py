from sqlalchemy import Column, Date, Integer, String, ForeignKey
from src.database import Base

class WorkPlanModel(Base):
    __tablename__ = "work_plans"

    id = Column(Integer, primary_key=True, index=True)
    brigade_id = Column(Integer, ForeignKey("brigades.id"))
    householder_id = Column(Integer, ForeignKey("householders.id"))
    task = Column(String, nullable=False)
    scheduled_time = Column(Date, nullable=False)