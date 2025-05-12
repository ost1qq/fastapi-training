from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.repositories.brigades import BrigadeRepository
from src.repositories.requests import RequestRepository
from src.database import get_session
from src.repositories.workplans import WorkPlanRepository
from src.schemas.workplans import WorkPlanCreate, WorkPlanUpdate
from src.api.auth import get_current_user
from src.schemas.users import User
from src.models.users import Role

router = APIRouter(prefix="/workplans", tags=["Work Plans"])

@router.get("/", summary="Get all work plans")
async def get_all_workplans(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await WorkPlanRepository.get_all(session)

@router.get("/{plan_id}", summary="Get work plan by ID")
async def get_workplan_by_id(
    plan_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        return await WorkPlanRepository.get_by_id(session, plan_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Work plan not found")

@router.post("/", summary="Create new work plan")
async def create_workplan(
    new_plan: WorkPlanCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    try:
        await RequestRepository.get_by_id(session, new_plan.request_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Request not found")
    
    try:
        await BrigadeRepository.get_by_id(session, new_plan.brigade_id)
    except NoResultFound:   
        raise HTTPException(status_code=404, detail="Brigade not found")

    plan = await WorkPlanRepository.create(session, new_plan)
    return {"message": "Work plan created", "plan": plan}

@router.put("/{plan_id}", summary="Update work plan")
async def update_workplan(
    plan_id: int,
    update_data: WorkPlanUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        await RequestRepository.get_by_id(session, update_data.request_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Request not found")

    try:
        await BrigadeRepository.get_by_id(session, update_data.brigade_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Brigade not found")

    try:
        updated = await WorkPlanRepository.update(session, plan_id, update_data)
        return {"message": "Work plan updated", "plan": updated}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Work plan not found")

    

@router.delete("/{plan_id}", summary="Delete work plan")
async def delete_workplan(
    plan_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != Role.DISPATCHER:
            raise HTTPException(status_code=403, detail="Forbidden")
        await WorkPlanRepository.delete(session, plan_id)
        return {"message": "Work plan deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Work plan not found")