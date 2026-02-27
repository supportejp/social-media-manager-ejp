from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    status: str = "draft"
    media_type: Optional[str] = None
    media_path: Optional[str] = None
    linkedin_post_urn: Optional[str] = None


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    linkedin_post_urn: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True