from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from src.models.users import Role
from src.api.auth import get_current_user
from src.schemas.users import User
from src.schemas.householder import HouseholderSchemaNew, HouseholderSchemaUpdate
from src.repositories.householder import (
    get_all_householders,
    get_householder_by_id,
    create_householder,
    update_householder,
    delete_householder,
    delete_all_householders
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session

router = APIRouter()

@router.get("/householders", tags=["Householders"], summary="Get all householders")
async def route_get_householders(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    print(current_user.role)
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await get_all_householders(session)

@router.get("/householders/{householder_id}", tags=["Householders"], summary="Get a specific householder")
async def route_get_householder(
    householder_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await get_householder_by_id(session, householder_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Householder not found")

@router.post("/householders", tags=["Householders"], summary="Create new householder")
async def route_create_householder(
    new_householder: HouseholderSchemaNew,
    session: AsyncSession = Depends(get_session)
):
    householder = await create_householder(session, new_householder)
    return {"message": "Householder created", "householder": householder}

@router.put("/householders/{householder_id}", tags=["Householders"], summary="Update an existing householder")
async def route_update_householder(
    householder_id: int,
    update_data: HouseholderSchemaUpdate,
    session: AsyncSession = Depends(get_session)
):
    try:
        householder = await update_householder(session, householder_id, update_data.dict(exclude_unset=True))
        return {"message": "Householder updated", "householder": householder}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Householder not found")

@router.delete("/householders/{householder_id}", tags=["Householders"], summary="Delete a specific householder")
async def route_delete_householder(
    householder_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        await delete_householder(session, householder_id)
        return {"message": "Householder deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Householder not found")

@router.delete("/householders", tags=["Householders"], summary="Delete all householders")
async def route_delete_all_householders(
    session: AsyncSession = Depends(get_session)
):
    await delete_all_householders(session)
    return {"message": "All householders deleted"}