from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

requests = []

class RequestCreate(BaseModel):
    householder_id: str
    work_type: str
    scale: str
    preferred_time: datetime

@router.post("/requests", tags=["Requests"], summary="Submit a new work request")
def create_request(new_request: RequestCreate):
    request_id = str(len(requests) + 1)
    request_data = new_request.dict()
    request_data["id"] = request_id
    request_data["status"] = "Pending"
    requests.append(request_data)
    return {"message": "Request submitted", "request": request_data}
