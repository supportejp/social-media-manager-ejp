from pydantic import BaseModel
from datetime import datetime

class CalendarItemBase(BaseModel):
    post_id: int
    account_id: int
    scheduled_at: datetime

class CalendarItemCreate(CalendarItemBase):
    pass

class CalendarItemResponse(CalendarItemBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True