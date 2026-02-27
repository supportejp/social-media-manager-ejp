from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AccountBase(BaseModel):
    name: str
    platform: str
    access_token: str | None = None
    urn: Optional[str] = None
    is_active: bool = True


class AccountCreate(AccountBase):
    pass


class AccountResponse(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime