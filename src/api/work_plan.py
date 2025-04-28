from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.api.request import requests
from src.api.brigade import brigades

router = APIRouter()

work_plan = []

class WorkAssignment(BaseModel):
    request_id: str
    brigade_id: str
    scheduled_time: datetime

@router.post("/work-plan", tags=["Work Plan"], summary="Assign a brigade to a request")
def assign_work(assignment: WorkAssignment):
    for req in requests:
        if req["id"] == assignment.request_id:
            for brigade in brigades:
                if brigade["id"] == assignment.brigade_id:
                    work_plan.append({
                        "request_id": assignment.request_id,
                        "brigade_id": assignment.brigade_id,
                        "scheduled_time": assignment.scheduled_time,
                        "status": "Scheduled"
                    })
                    req["status"] = "Scheduled"
                    return {"message": "Work scheduled", "work": work_plan[-1]}
            raise HTTPException(status_code=404, detail="Brigade not found")
    raise HTTPException(status_code=404, detail="Request not found")
