from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SqlEnum
from src.database import Base
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.requests import RequestModel

class Role(str, Enum):
    HOUSEHOLDER = "HOUSEHOLDER"
    DISPATCHER = "DISPATCHER"

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str]
    role: Mapped[Role] = mapped_column(SqlEnum(Role))

    requests: Mapped[list["RequestModel"]] = relationship(back_populates="user")
