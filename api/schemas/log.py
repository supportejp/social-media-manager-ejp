from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    level: str
    event: str
    message: str | None = None

    schedule_id: int | None = None
    calendar_item_id: int | None = None
    post_id: int | None = None
    account_id: int | None = None

    created_at: datetime