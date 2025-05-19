from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.database import get_session
from app.repositories.brigades import BrigadeRepository
from app.schemas.brigades import Brigade, BrigadeUpdate

#must be reworked
from app.api.auth import get_current_user
from app.schemas.users import User
from app.models.users import Role

router = APIRouter(prefix="/brigades", tags=["Brigades"])

@router.get("/", summary="Get all brigades")
async def get_all_brigades(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await BrigadeRepository.get_all(session)

@router.get("/{brigade_id}", summary="Get brigade by ID")
async def get_brigade(
    brigade_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        return await BrigadeRepository.get_by_id(session, brigade_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Brigade not found")

@router.post("/", summary="Create new brigade")
async def create_brigade(
    new_brigade: Brigade,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    brigade = await BrigadeRepository.create(session, new_brigade)
    return {"message": "Brigade created", "brigade": brigade}

@router.put("/{brigade_id}", summary="Update brigade")
async def update_brigade(
    brigade_id: int,
    update_data: BrigadeUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != Role.DISPATCHER:
            raise HTTPException(status_code=403, detail="Forbidden")
        updated = await BrigadeRepository.update(session, brigade_id, update_data)
        return {"message": "Brigade updated", "brigade": updated}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Brigade not found")

@router.delete("/{brigade_id}", summary="Delete brigade")
async def delete_brigade(
    brigade_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != Role.DISPATCHER:
            raise HTTPException(status_code=403, detail="Forbidden")
        await BrigadeRepository.delete(session, brigade_id)
        return {"message": "Brigade deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Brigade not found")

@router.delete("/", summary="Delete all brigades")
async def delete_all_brigades(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    await BrigadeRepository.delete_all(session)
    return {"message": "All brigades deleted"}
