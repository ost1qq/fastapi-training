from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models.users import UserModel
from app.schemas.users import User

router = APIRouter()

security = HTTPBasic()

@router.post("/auth", summary="Check user credentials")
async def auth_user(
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
