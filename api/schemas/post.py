from pydantic import BaseModel, ConfigDict
from datetime import datetime
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime