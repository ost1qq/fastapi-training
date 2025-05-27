import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TypeDecorator, TEXT
from database_core import Base


class JSONEncodedList(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

class Brigade(Base):
    __tablename__ = "brigades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    workers = Column(JSONEncodedList, nullable=False)
