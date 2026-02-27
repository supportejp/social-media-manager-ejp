from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CalendarItemBase(BaseModel):
    post_id: int
    account_id: int
    scheduled_at: datetime


class CalendarItemCreate(CalendarItemBase):
    pass


class CalendarItemResponse(CalendarItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime