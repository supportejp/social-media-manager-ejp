from pydantic import BaseModel
from datetime import datetime

class LogResponse(BaseModel):
    id: int
    level: str
    event: str
    message: str | None = None

    schedule_id: int | None = None
    calendar_item_id: int | None = None
    post_id: int | None = None
    account_id: int | None = None

    created_at: datetime

    class Config:
        orm_mode = True