from fastapi import APIRouter

from schemas.request import RequestCreate

router = APIRouter(tags=["Requests"])

requests = []


@router.get("/requests", summary="Submit a new work request")
def get_requests():
    return {"data": requests}


@router.post("/requests", summary="Submit a new work request")
def create_request(new_request: RequestCreate):
    request_id = str(len(requests) + 1)
    request_data = new_request.dict()
    request_data["id"] = request_id
    request_data["status"] = "Pending"
    requests.append(request_data)
    return {"message": "Request submitted", "request": request_data}
