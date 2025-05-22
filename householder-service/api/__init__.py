from fastapi import APIRouter

from api.householder import router

main_router = APIRouter()

main_router.include_router(router)
