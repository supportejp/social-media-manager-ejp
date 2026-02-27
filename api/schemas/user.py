from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = "owner"


class UserCreate(UserBase):
    password: str
    organization_id: int


class UserResponse(UserBase):
    id: int
    organization_id: int

    class Config:
        orm_mode = True