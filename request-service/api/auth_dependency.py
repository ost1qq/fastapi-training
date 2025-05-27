from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import httpx

security = HTTPBasic()

async def current_dispatcher(
    credentials: HTTPBasicCredentials = Depends(security),
) -> None:
    auth = httpx.BasicAuth(username=credentials.username, password=credentials.password)

    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get("http://auth-service:8001/get_current_user")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Unauthorized")
        data = response.json()
        print(data)
        role = data.get("data", {}).get("role")
        if role != "DISPATCHER":
            raise HTTPException(status_code=403, detail="Forbidden")
    return response.json()

async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> None:
    auth = httpx.BasicAuth(username=credentials.username, password=credentials.password)

    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get("http://auth-service:8001/get_current_user")
    return response.json()
