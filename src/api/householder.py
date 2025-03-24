from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

householders = [
    {"id": "1", "name": "John Doe"},
    {"id": "2", "name": "Jane Doe"}
]

class NewHouseholder(BaseModel):
    name: str


@router.get("/householders", tags=["Householders"], summary="Get all householders")
def get_householders():
    return householders

@router.get("/householders/{householder_id}", tags=["Householders"], summary="Get a specific householder")
def get_householder(householder_id: str):
    for householder in householders:
        if householder["id"] == householder_id:
            return householder
    raise HTTPException(status_code=404, detail="Householder was not found.")

@router.post("/householders", tags=["Householders"], summary="Create new householder")
def post_householder(new_householder: NewHouseholder):
    householders.append({
        "id": len(householders) + 1,
        "name": new_householder.name
    })
    return {"success": True}

@router.put("/householders/{householder_id}", tags=["Householders"], summary="Create new householder")
def put_householder(householder_id: str, update_householder: NewHouseholder):
    for index, householder in enumerate(householders):
        if householder["id"] == householder_id:
            householders[index].update(update_householder)
            return {"message": "Householder was updated", "data": householder[index]}
    raise HTTPException(status_code=404, detail="Householder was not found.")

@router.delete("/householders}", tags=["Householders"], summary="Delete all householders")
def delete_householders():
    global householders
    householders = []
    return

@router.delete("/householder/{householder_id}", tags=["Householders"], summary="Delete a specific householders")
def delete_householder(householder_id: str):
    for index, householder in enumerate(householders):
        if householder["id"] == householder_id:
            del householder[index]
            return
    raise HTTPException(status_code=404, detail="Householder was not found.")