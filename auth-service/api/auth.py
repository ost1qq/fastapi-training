from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database_core import get_session
from models.users import UserModel, Role
from schemas.users import User

security = HTTPBasic()
router = APIRouter(tags=["Auth"])

async def get_user(
    role: str | None = None,
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    where_stmt_lst = [
        UserModel.username == credentials.username,
    ]
    if role:
        where_stmt_lst.append(UserModel.role == role)
    stmt = select(UserModel).where(and_(*where_stmt_lst))
    result = await session.execute(stmt)
    user_obj = result.scalar_one_or_none()

    if not user_obj or user_obj.password != user_obj.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return User(
        id=user_obj.id,
        username=user_obj.username,
        role=user_obj.role,
    )

async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await get_user(credentials=credentials, session=session)

async def get_dispatcher(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await get_user(
        role=Role.DISPATCHER, credentials=credentials, session=session
    )

async def get_householder(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await get_user(
        role=Role.HOUSEHOLDER, credentials=credentials, session=session
    )

@router.get("/get_current_user")
def is_active_user(user: Annotated[User, Depends(get_current_user)]):
    return {"data": user}

@router.get("/get_current_dispatcher")
def is_active_user(user: Annotated[User, Depends(get_dispatcher)]):
    return {"data": user}

@router.get("/get_current_householder")
def is_active_user(user: Annotated[User, Depends(get_householder)]):
    return {"data": user}
