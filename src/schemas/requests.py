from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

def strip_tzinfo(value):
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    if isinstance(value, datetime) and value.tzinfo:
        return value.replace(tzinfo=None)
    return value

class RequestCreate(BaseModel):
    work_type: str
    scale: str
    preferred_time: datetime

    @validator("preferred_time", pre=True)
    def validate_preferred_time(cls, v):
        return strip_tzinfo(v)

class RequestUpdate(BaseModel):
    work_type: Optional[str] = None
    scale: Optional[str] = None
    preferred_time: Optional[datetime] = None

    @validator("preferred_time", pre=True)
    def validate_preferred_time(cls, v):
        return strip_tzinfo(v)
