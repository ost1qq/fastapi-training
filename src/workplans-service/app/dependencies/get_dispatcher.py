from fastapi import Depends, HTTPException
from app.services.auth import get_current_user
from app.schemas.users import User, Role

def get_dispatcher(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.DISPATCHER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user
