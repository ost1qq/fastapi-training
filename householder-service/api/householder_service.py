from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from models.householders import HouseholderModel
from schemas.householder import HouseholderSchemaNew, HouseholderSchemaUpdate


async def get_all_householders(session: AsyncSession):
    query = select(HouseholderModel)
    result = await session.execute(query)
    return result.scalars().all()


async def get_householder_by_id(session: AsyncSession, householder_id: int):
    query = select(HouseholderModel).where(HouseholderModel.id == householder_id)
    result = await session.execute(query)
    householder = result.scalars().first()
    if not householder:
        raise NoResultFound("Householder not found")
    return householder


async def create_householder(
    session: AsyncSession, new_householder: HouseholderSchemaNew
):
    householder = HouseholderModel(**new_householder.dict())
    session.add(householder)
    await session.commit()
    await session.refresh(householder)
    return householder


async def update_householder(
    session: AsyncSession, householder_id: int, update_data: HouseholderSchemaUpdate
):
    householder = await get_householder_by_id(session, householder_id)
    for key, value in update_data.items():
        setattr(householder, key, value)
    await session.commit()
    await session.refresh(householder)
    return householder


async def delete_householder(session: AsyncSession, householder_id: int):
    householder = await get_householder_by_id(session, householder_id)
    await session.delete(householder)
    await session.commit()


async def delete_all_householders(session: AsyncSession):
    await session.execute(HouseholderModel.__table__.delete())
    await session.commit()
