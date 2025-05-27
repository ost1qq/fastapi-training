from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enums.work_plan_status import WorkPlanStatus

class WorkPlanCreate(BaseModel):
    brigade_id: int
    request_id: int
    scheduled_time: datetime

class WorkPlanRead(BaseModel):
    id: int
    brigade_id: int
    request_id: int
    scheduled_time: datetime
    status: WorkPlanStatus

    class Config:
        from_attributes = True

class WorkPlanUpdate(BaseModel):
    brigade_id: Optional[int] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[WorkPlanStatus] = None

    class Config:
        from_attributes = True
