from src.schemas.requests import RequestCreate
from src.models.requests import RequestModel
from src.repositories.base import BaseRepository

class RequestRepository(BaseRepository):
    model = RequestModel

    @classmethod
    async def create(cls, session, data: RequestCreate, user_id: int):
        instance = cls.model(**data.dict(), user_id=user_id)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance