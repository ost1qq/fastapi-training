from datetime import datetime
import httpx
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from api.auth_dependency import current_dispatcher


security = HTTPBasic()

router = APIRouter(tags=["Work Plan"], dependencies=[Security(current_dispatcher)])

work_plan = []


class WorkAssignment(BaseModel):
    request_id: str
    brigade_id: str
    scheduled_time: datetime


@router.get("/work-plans", summary="Assign a brigade to a request")
async def get_work_plans():
    return {"data": work_plan}


@router.post("/work-plan", summary="Assign a brigade to a request")
async def assign_work(
    assignment: WorkAssignment,
    credentials: HTTPBasicCredentials = Depends(security),
):
    auth = httpx.BasicAuth(username=credentials.username, password=credentials.password)
    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get("http://request-service:8004/requests")
        requests = response.json().get("data", [])

        response = await client.get("http://brigade-service:8003/brigades")
        brigades = response.json().get("data", [])

    for req in requests:
        if req["id"] == assignment.request_id:
            for brigade in brigades:
                if brigade["id"] == assignment.brigade_id:
                    work_plan.append(
                        {
                            "request_id": assignment.request_id,
                            "brigade_id": assignment.brigade_id,
                            "scheduled_time": assignment.scheduled_time,
                            "status": "Scheduled",
                        }
                    )
                    req["status"] = "Scheduled"
                    return {"message": "Work scheduled", "work": work_plan[-1]}
            raise HTTPException(status_code=404, detail="Brigade not found")
    raise HTTPException(status_code=404, detail="Request not found")
