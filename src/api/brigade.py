from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Brigades"])

brigades = []


class BrigadeCreate(BaseModel):
    name: str
    workers: List[str]


@router.post("/brigades", summary="Create a new brigade")
def create_brigade(new_brigade: BrigadeCreate):
    brigade_id = str(len(brigades) + 1)
    brigade_data = new_brigade.dict()
    brigade_data["id"] = brigade_id
    brigades.append(brigade_data)
    return {"message": "Brigade created", "brigade": brigade_data}
