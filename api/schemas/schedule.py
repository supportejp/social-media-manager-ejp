from pydantic import BaseModel
from datetime import datetime

class ScheduleBase(BaseModel):
    calendar_item_id: int
    status: str = "pending"
    executed_at: datetime | None = None

class ScheduleResponse(ScheduleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True