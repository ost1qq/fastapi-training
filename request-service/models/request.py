from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from enums.requests_status import RequestStatus
from database_core import Base
from datetime import datetime

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    work_type = Column(String, nullable=False)
    scale = Column(String, nullable=False)
    preferred_time = Column(DateTime(timezone=True), default=datetime.utcnow)
    status = Column(SqlEnum(RequestStatus), default=RequestStatus.pending, nullable=False)
