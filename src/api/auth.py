from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_session
from src.models.users import UserModel
from src.schemas.users import User

security = HTTPBasic()

async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    stmt = select(UserModel).where(UserModel.username == credentials.username)
    result = await session.execute(stmt)
    user_obj = result.scalar_one_or_none()

    if not user_obj or user_obj.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return User(
        id=user_obj.id,
        username=user_obj.username,
        password=user_obj.password,
        role=user_obj.role
    )
