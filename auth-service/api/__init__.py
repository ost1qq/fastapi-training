from fastapi import APIRouter

from api.auth import router

main_router = APIRouter()

main_router.include_router(router)
