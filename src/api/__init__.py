from fastapi import APIRouter

from src.api.householder import router as householder_router
from src.api.brigade import router as brigade_router
from src.api.work_plan import router as work_plan

main_router = APIRouter()

main_router.include_router(householder_router)