from fastapi import APIRouter

from src.api.requests import router as request_router
from src.api.brigades import router as brigade_router
from src.api.workplans import router as workplan_router

main_router = APIRouter()

main_router.include_router(request_router)
main_router.include_router(brigade_router)
main_router.include_router(workplan_router)
