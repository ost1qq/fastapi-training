from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    HOUSEHOLDER = "HOUSEHOLDER"
    DISPATCHER = "DISPATCHER"

class User(BaseModel):
    username: str
    password: str
    role: Role
