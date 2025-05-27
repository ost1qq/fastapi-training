from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database_core import get_session
from models.brigade import Brigade
from schemas.brigade import BrigadeCreate, BrigadeRead
from api.auth_dependency import current_dispatcher
from schemas.brigade import BrigadeUpdate

router = APIRouter(tags=["Brigades"], dependencies=[Security(current_dispatcher)])

@router.get("/brigades", summary="Get all brigades", response_model=dict)
async def get_brigades(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Brigade))
    brigades = result.scalars().all()
    return {"data": [BrigadeRead.from_orm(b) for b in brigades]}

@router.post("/brigades", summary="Create a new brigade", response_model=dict)
async def create_brigade(
    new_brigade: BrigadeCreate,
    session: AsyncSession = Depends(get_session)
):
    brigade_obj = Brigade(**new_brigade.dict())
    session.add(brigade_obj)
    await session.commit()
    await session.refresh(brigade_obj)
    return {"message": "Brigade created", "brigade": BrigadeRead.from_orm(brigade_obj)}

@router.get("/brigades/{brigade_id}", summary="Get a brigade by ID", response_model=BrigadeRead)
async def get_brigade(brigade_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Brigade).where(Brigade.id == brigade_id))
    brigade = result.scalars().first()
    if not brigade:
        raise HTTPException(status_code=404, detail="Brigade not found")
    return BrigadeRead.from_orm(brigade)

@router.put("/brigades/{brigade_id}", summary="Update a brigade", response_model=BrigadeRead)
async def update_brigade(
    brigade_id: int,
    updated_data: BrigadeUpdate,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Brigade).where(Brigade.id == brigade_id))
    brigade = result.scalars().first()
    if not brigade:
        raise HTTPException(status_code=404, detail="Brigade not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(brigade, key, value)

    await session.commit()
    await session.refresh(brigade)
    return BrigadeRead.from_orm(brigade)

@router.delete("/brigades/{brigade_id}", summary="Delete a brigade", response_model=dict)
async def delete_brigade(brigade_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Brigade).where(Brigade.id == brigade_id))
    brigade = result.scalars().first()
    if not brigade:
        raise HTTPException(status_code=404, detail="Brigade not found")

    await session.delete(brigade)
    await session.commit()
    return {"message": "Brigade deleted"}
