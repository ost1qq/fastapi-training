from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import httpx

security = HTTPBasic()


async def current_dispatcher(
    credentials: HTTPBasicCredentials = Depends(security),
) -> None:
    auth = httpx.BasicAuth(username=credentials.username, password=credentials.password)

    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get("http://auth-service:8001/get_current_dispatcher")

        if not response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Credentials")
    return response.json()
