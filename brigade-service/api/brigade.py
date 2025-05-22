from fastapi import APIRouter
from schemas.brigade import BrigadeCreate

router = APIRouter(tags=["Brigades"])

brigades = []


@router.get("/brigades")
def get_brigades():
    return {"data": brigades}


@router.post("/brigades", summary="Create a new brigade")
def create_brigade(new_brigade: BrigadeCreate):
    brigade_id = str(len(brigades) + 1)
    brigade_data = new_brigade.dict()
    brigade_data["id"] = brigade_id
    brigades.append(brigade_data)
    return {"message": "Brigade created", "brigade": brigade_data}


# router = APIRouter()

work_plan = []


# @router.post("/work-plan", tags=["Work Plan"], summary="Assign a brigade to a request")
# def assign_work(assignment: WorkAssignment):
#     for req in requests:
#         if req["id"] == assignment.request_id:
#             for brigade in brigades:
#                 if brigade["id"] == assignment.brigade_id:
#                     work_plan.append(
#                         {
#                             "request_id": assignment.request_id,
#                             "brigade_id": assignment.brigade_id,
#                             "scheduled_time": assignment.scheduled_time,
#                             "status": "Scheduled",
#                         }
#                     )
#                     req["status"] = "Scheduled"
#                     return {"message": "Work scheduled", "work": work_plan[-1]}
#             raise HTTPException(status_code=404, detail="Brigade not found")
#     raise HTTPException(status_code=404, detail="Request not found")
