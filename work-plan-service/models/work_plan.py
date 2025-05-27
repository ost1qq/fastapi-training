from sqlalchemy import Column, Integer, DateTime, Enum as SqlEnum
from database_core import Base
from datetime import datetime
from enums.work_plan_status import WorkPlanStatus

class WorkPlan(Base):
    __tablename__ = "work_plans"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, nullable=False)
    brigade_id = Column(Integer, nullable=False)
    scheduled_time = Column(DateTime(timezone=True), default=datetime.utcnow)
    status = Column(SqlEnum(WorkPlanStatus), default=WorkPlanStatus.scheduled, nullable=False)
