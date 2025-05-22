from datetime import datetime
from typing import List
from pydantic import BaseModel


class BrigadeCreate(BaseModel):
    name: str
    workers: List[str]


class WorkAssignment(BaseModel):
    request_id: str
    brigade_id: str
    scheduled_time: datetime
