from pydantic import BaseModel

class WorkPlanCreate(BaseModel):
    brigade_id: int
    request_id: int

class WorkPlanUpdate(BaseModel):
    brigade_id: int | None = None
    request_id: int | None = None 

