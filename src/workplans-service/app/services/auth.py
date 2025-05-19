import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas.users import User

security = HTTPBasic()

USERS_SERVICE_URL = "http://users-service:8000"

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USERS_SERVICE_URL}/auth",
            auth=(credentials.username, credentials.password),
        )

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return User(**response.json())