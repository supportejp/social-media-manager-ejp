from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import Base
from api.models.post import Post
from api.schemas.post import PostCreate, PostResponse
from api.core.dependencies import get_db
from api.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    org_id = current_user["organization_id"]

    db_post = Post(
        **post.dict(),
        organization_id=org_id
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    org_id = current_user["organization_id"]

    return db.query(Post).filter(
        Post.organization_id == org_id
    ).all()