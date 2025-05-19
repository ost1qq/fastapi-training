from app.models.workplans import WorkPlanModel
from app.repositories.base import BaseRepository

class WorkPlanRepository(BaseRepository):
    model = WorkPlanModel
