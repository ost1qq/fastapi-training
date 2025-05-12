from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from src.database import get_session
from src.repositories.requests import RequestRepository
from src.schemas.requests import RequestCreate, RequestUpdate
from src.api.auth import get_current_user
from src.schemas.users import User
from src.models.users import Role

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.get("/", summary="Get all requests")
async def get_all_requests(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await RequestRepository.get_all(session)

@router.get("/{request_id}", summary="Get request by ID")
async def get_request(
    request_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        return await RequestRepository.get_by_id(session, request_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Request not found")

@router.post("/", summary="Create new request")
async def create_request(
    new_request: RequestCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.HOUSEHOLDER:
        raise HTTPException(status_code=403, detail="Forbidden")

    request = await RequestRepository.create(session, new_request, user_id=current_user.id)
    return {"message": "Request created", "request": request}

@router.put("/{request_id}", summary="Update a request")
async def update_request(
    request_id: int,
    update_data: RequestUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        existing_request = await RequestRepository.get_by_id(session, request_id)
        if current_user.role != Role.DISPATCHER and existing_request.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        updated = await RequestRepository.update(session, request_id, update_data)
        return {"message": "Request updated", "request": updated}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Request not found")

@router.delete("/{request_id}", summary="Delete request")
async def delete_request(
    request_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        request = await RequestRepository.get_by_id(session, request_id)
        if current_user.role != Role.DISPATCHER and request.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        await RequestRepository.delete(session, request_id)
        return {"message": "Request deleted"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Request not found")

@router.delete("/", summary="Delete all requests")
async def delete_all_requests(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    await RequestRepository.delete_all(session)
    return {"message": "All requests deleted"}
