from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enums.requests_status import RequestStatus

class RequestCreate(BaseModel):
    work_type: str
    scale: str
    preferred_time: datetime

class RequestUpdate(BaseModel):
    work_type: Optional[str]
    scale: Optional[str]
    preferred_time: Optional[datetime]

    class Config:
        from_attributes = True

class RequestRead(BaseModel):
    id: int
    work_type: str
    scale: str
    preferred_time: datetime
    status: RequestStatus

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: RequestStatus