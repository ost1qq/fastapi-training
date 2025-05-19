import httpx
from fastapi import HTTPException

REQUESTS_SERVICE_URL = "http://requests-service:8000"
BRIGADES_SERVICE_URL = "http://brigades-service:8000"

async def validate_request_exists(request_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{REQUESTS_SERVICE_URL}/requests/{request_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Request not found")

async def validate_brigade_exists(brigade_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BRIGADES_SERVICE_URL}/brigades/{brigade_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Brigade not found")
