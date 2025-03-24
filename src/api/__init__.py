from fastapi import APIRouter

from src.api.householder import router as householder_router

main_router = APIRouter()

main_router.include_router(householder_router)