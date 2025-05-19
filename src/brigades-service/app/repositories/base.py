from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, obj_id: int):
        result = await session.execute(select(cls.model).where(cls.model.id == obj_id))
        instance = result.scalars().first()
        if not instance:
            raise NoResultFound(f"{cls.model.__name__} not found")
        return instance

    @classmethod
    async def create(cls, session: AsyncSession, data):
        instance = cls.model(**data.dict())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def update(cls, session: AsyncSession, obj_id: int, update_data):
        instance = await cls.get_by_id(session, obj_id)
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(instance, key, value)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def delete(cls, session: AsyncSession, obj_id: int):
        instance = await cls.get_by_id(session, obj_id)
        await session.delete(instance)
        await session.commit()

    @classmethod
    async def delete_all(cls, session: AsyncSession):
        await session.execute(cls.model.__table__.delete())
        await session.commit()
