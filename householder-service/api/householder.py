from typing import Annotated
from fastapi import APIRouter, Depends, Security, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from api.auth_dependency import current_dispatcher
from schemas.householder import HouseholderSchemaNew, HouseholderSchemaUpdate
from api.householder_service import (
    get_all_householders,
    get_householder_by_id,
    create_householder,
    update_householder,
    delete_householder,
    delete_all_householders,
)
from database_core import get_session

router = APIRouter(tags=["Householders"], dependencies=[Security(current_dispatcher)])


@router.get("/householders", summary="Get all householders")
async def route_get_householders(
    session: AsyncSession = Depends(get_session),
):

    return await get_all_householders(session)


@router.get(
    "/householders/{householder_id}",
    summary="Get a specific householder",
)
async def route_get_householder(
    householder_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        return await get_householder_by_id(session, householder_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Householder not found")


@router.post("/householders", summary="Create new householder")
async def route_create_householder(
    new_householder: HouseholderSchemaNew, session: AsyncSession = Depends(get_session)
):
    householder = await create_householder(session, new_householder)
    return {"message": "Householder created", "householder": householder}


@router.put(
    "/householders/{householder_id}",
    summary="Update an existing householder",
)
async def route_update_householder(
    householder_id: int,
    update_data: HouseholderSchemaUpdate,
    session: AsyncSession = Depends(get_session),
):
    try:
        householder = await update_householder(
            session, householder_id, update_data.dict(exclude_unset=True)
        )
        return {"message": "Householder updated", "householder": householder}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Householder not found")


@router.delete(
    "/householders/{householder_id}",
    summary="Delete a specific householder",
)
async def route_delete_householder(
    householder_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        await delete_householder(session, householder_id)
        return {"message": "Householder deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Householder not found")


@router.delete("/householders", summary="Delete all householders")
async def route_delete_all_householders(session: AsyncSession = Depends(get_session)):
    await delete_all_householders(session)
    return {"message": "All householders deleted"}
