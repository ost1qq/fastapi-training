from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.database import get_session
from app.repositories.workplans import WorkPlanRepository
from app.schemas.workplans import WorkPlanCreate, WorkPlanUpdate
from app.services.external_validators import validate_request_exists, validate_brigade_exists
from app.dependencies.get_dispatcher import get_dispatcher
from app.schemas.users import User

router = APIRouter(prefix="/workplans", tags=["Work Plans"])

@router.get("/", summary="Get all work plans")
async def get_all_workplans(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_dispatcher)
):
    return await WorkPlanRepository.get_all(session)

@router.get("/{plan_id}", summary="Get work plan by ID")
async def get_workplan_by_id(
    plan_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_dispatcher)
):
    try:
        return await WorkPlanRepository.get_by_id(session, plan_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Work plan not found")

@router.post("/", summary="Create new work plan")
async def create_workplan(
    new_plan: WorkPlanCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_dispatcher)
):
    await validate_request_exists(new_plan.request_id)
    await validate_brigade_exists(new_plan.brigade_id)

    plan = await WorkPlanRepository.create(session, new_plan)
    return {"message": "Work plan created", "plan": plan}

@router.put("/{plan_id}", summary="Update work plan")
async def update_workplan(
    plan_id: int,
    update_data: WorkPlanUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_dispatcher)
):
    await validate_request_exists(update_data.request_id)
    await validate_brigade_exists(update_data.brigade_id)

    try:
        updated = await WorkPlanRepository.update(session, plan_id, update_data)
        return {"message": "Work plan updated", "plan": updated}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Work plan not found")

@router.delete("/{plan_id}", summary="Delete work plan")
async def delete_workplan(
    plan_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_dispatcher)
):
    try:
        await WorkPlanRepository.delete(session, plan_id)
        return {"message": "Work plan deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Work plan not found")
