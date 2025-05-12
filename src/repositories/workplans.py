from src.models.workplans import WorkPlanModel
from src.repositories.base import BaseRepository

class WorkPlanRepository(BaseRepository):
    model = WorkPlanModel
