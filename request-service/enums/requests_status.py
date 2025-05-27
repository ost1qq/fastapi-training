from enum import Enum

class RequestStatus(str, Enum):
    pending = "Pending"
    rejected = "Rejected"
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"
