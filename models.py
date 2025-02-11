from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CallStatus(Enum):
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    QUEUED = "queued"


class CallRequest(BaseModel):
    to_number: str
    message: Optional[str] = None
