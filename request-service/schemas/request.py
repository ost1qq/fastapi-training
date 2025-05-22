from datetime import datetime
from pydantic import BaseModel


class RequestCreate(BaseModel):
    householder_id: str
    work_type: str
    scale: str
    preferred_time: datetime
