from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = "owner"


class UserCreate(UserBase):
    password: str
    organization_id: int


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int