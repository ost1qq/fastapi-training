from pydantic import BaseModel

class Brigade(BaseModel):
    name: str
    worker_count: int

class BrigadeUpdate(BaseModel):
    name: str | None = None
    worker_count: int | None = None