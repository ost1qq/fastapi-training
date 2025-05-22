from sqlalchemy.orm import Mapped, mapped_column
from database_core import Base


class HouseholderModel(Base):
    __tablename__ = "householders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    flat_num: Mapped[int]
