from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database_core import get_session
from models.request import Request
from schemas.request import RequestCreate, RequestRead, RequestUpdate
from schemas.request import StatusUpdate
from api.auth_dependency import get_current_user

router = APIRouter(tags=["Requests"])

@router.get("/requests", summary="Get all work requests", response_model=dict)
async def get_requests(session: AsyncSession = Depends(get_session), user: dict = Depends(get_current_user)):
    if user["data"]["role"] != "DISPATCHER":
        raise HTTPException(status_code=403, detail="Forbidden: Only dispatchers can view all requests")
    result = await session.execute(select(Request))
    requests = result.scalars().all()
    return {"data": [RequestRead.from_orm(r) for r in requests]}

@router.get("/requests/{request_id}", summary="Get a request by ID", response_model=RequestRead)
async def get_request_by_id(request_id: int, session: AsyncSession = Depends(get_session), user: dict = Depends(get_current_user)):
    
    result = await session.execute(select(Request).where(Request.id == request_id))
    request_obj = result.scalars().first()
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    if user["data"]["id"] != request_obj.user_id and user["data"]["role"] != "DISPATCHER":
        raise HTTPException(status_code=403, detail="Forbidden: Only the request owner or dispatchers can update the request")
    return RequestRead.from_orm(request_obj)

@router.post("/requests", summary="Submit a new work request", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_request(
    new_request: RequestCreate,
    session: AsyncSession = Depends(get_session), user: dict = Depends(get_current_user)
):
    print("User from token:", user)

    request_obj = Request(**new_request.dict(), user_id = user["data"]["id"])
    session.add(request_obj)
    await session.commit()
    await session.refresh(request_obj)
    return {"message": "Request submitted", "request": RequestRead.from_orm(request_obj)}

@router.patch("/requests/{request_id}/status", summary="Update request status", response_model=RequestRead)
async def update_request_status(
    request_id: int,
    status_update: StatusUpdate,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    result = await session.execute(select(Request).where(Request.id == request_id))
    request_obj = result.scalars().first()

    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")

    if user["data"]["role"] != "DISPATCHER":
        raise HTTPException(status_code=403, detail="Forbidden: Only dispatchers can update request status")
    
    request_obj.status = status_update.status
    await session.commit()
    await session.refresh(request_obj)

    return RequestRead.from_orm(request_obj)

@router.put("/requests/{request_id}", summary="Update a request by ID", response_model=RequestRead)
async def update_request(
    request_id: int,
    updated_data: RequestUpdate,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user)
):
    result = await session.execute(select(Request).where(Request.id == request_id))
    request_obj = result.scalars().first()
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if user["data"]["id"] != request_obj.user_id and user["data"]["role"] != "DISPATCHER":
        raise HTTPException(status_code=403, detail="Forbidden: Only the request owner or dispatchers can update the request")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(request_obj, key, value)

    await session.commit()
    await session.refresh(request_obj)
    return RequestRead.from_orm(request_obj)

@router.delete("/requests/{request_id}", summary="Delete a request by ID", response_model=dict)
async def delete_request(request_id: int, session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user)):
    result = await session.execute(select(Request).where(Request.id == request_id))
    request_obj = result.scalars().first()
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")

    if user["data"]["id"] != request_obj.user_id and user["data"]["role"] != "DISPATCHER":
        raise HTTPException(status_code=403, detail="Forbidden: Only the request owner or dispatchers can delete the request")

    await session.delete(request_obj)
    await session.commit()
    return {"message": f"Request with id {request_id} has been deleted"}
