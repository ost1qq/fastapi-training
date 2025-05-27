import httpx
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database_core import get_session
from models.work_plan import WorkPlan
from schemas.work_plan import WorkPlanCreate, WorkPlanRead
from api.auth_dependency import current_dispatcher
from schemas.work_plan import WorkPlanUpdate

security = HTTPBasic()

router = APIRouter(tags=["Work Plan"], dependencies=[Security(current_dispatcher)])

@router.get("/work-plans", summary="Get all scheduled work", response_model=dict)
async def get_work_plans(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WorkPlan))
    plans = result.scalars().all()
    return {"data": [WorkPlanRead.from_orm(p) for p in plans]}

@router.post("/work-plan", summary="Assign a brigade to a request", response_model=dict)
async def assign_work(
    assignment: WorkPlanCreate,
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    auth = httpx.BasicAuth(username=credentials.username, password=credentials.password)
    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get("http://request-service:8004/requests")
        requests = response.json().get("data", [])

        response = await client.get("http://brigade-service:8003/brigades")
        brigades = response.json().get("data", [])

    request_exists = any(req["id"] == assignment.request_id for req in requests)
    brigade_exists = any(b["id"] == assignment.brigade_id for b in brigades)

    if not request_exists:
        raise HTTPException(status_code=404, detail="Request not found")
    if not brigade_exists:
        raise HTTPException(status_code=404, detail="Brigade not found")

    work = WorkPlan(
        request_id=assignment.request_id,
        brigade_id=assignment.brigade_id,
        scheduled_time=assignment.scheduled_time,
        status="Scheduled"
    )
    session.add(work)
    await session.commit()
    await session.refresh(work)

    return {"message": "Work scheduled", "work": WorkPlanRead.from_orm(work)}

@router.get("/work-plan/{plan_id}", summary="Get work plan by ID", response_model=WorkPlanRead)
async def get_work_plan(plan_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WorkPlan).where(WorkPlan.id == plan_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Work plan not found")
    return WorkPlanRead.from_orm(plan)

@router.put("/work-plan/{plan_id}", summary="Update a work plan", response_model=WorkPlanRead)
async def update_work_plan(
    plan_id: int,
    updated_data: WorkPlanUpdate,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(WorkPlan).where(WorkPlan.id == plan_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Work plan not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(plan, key, value)

    await session.commit()
    await session.refresh(plan)
    return WorkPlanRead.from_orm(plan)

@router.delete("/work-plan/{plan_id}", summary="Delete a work plan", response_model=dict)
async def delete_work_plan(plan_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(WorkPlan).where(WorkPlan.id == plan_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Work plan not found")

    await session.delete(plan)
    await session.commit()
    return {"message": "Work plan deleted"}
