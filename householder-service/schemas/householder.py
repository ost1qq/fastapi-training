from pydantic import BaseModel


class HouseholderSchemaNew(BaseModel):
    name: str
    flat_num: int


class HouseholderSchemaUpdate(BaseModel):
    name: str | None = None
    flat_num: int | None = None
