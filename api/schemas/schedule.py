from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ScheduleBase(BaseModel):
    calendar_item_id: int
    status: str = "pending"
    executed_at: datetime | None = None


class ScheduleResponse(ScheduleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime