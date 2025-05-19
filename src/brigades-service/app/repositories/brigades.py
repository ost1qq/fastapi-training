from app.models.brigades import BrigadeModel
from app.repositories.base import BaseRepository

class BrigadeRepository(BaseRepository):
    model = BrigadeModel
