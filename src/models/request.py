from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class RequestModel(Base):
	__tablename__ = "requests"

	id: Mapped[int] = mapped_column(primary_key=True)
	householder_id: Mapped[int] = mapped_column(foreign_key("householders.id"))