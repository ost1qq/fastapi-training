from typing import List, Optional
from pydantic import BaseModel

class BrigadeCreate(BaseModel):
    name: str
    workers: List[str]

class BrigadeRead(BaseModel):
    id: int
    name: str
    workers: List[str]

    class Config:
        from_attributes = True

class BrigadeUpdate(BaseModel):
    name: Optional[str] = None
    workers: Optional[List[str]] = None

    class Config:
        from_attributes = True
