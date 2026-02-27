from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.models.calendar_item import CalendarItem
from api.models.post import Post
from api.models.account import Account
from api.models.schedule import Schedule

from api.schemas.calendar_item import CalendarItemCreate, CalendarItemResponse
from api.core.dependencies import get_db
from shared.time_utils import to_utc_naive
from api.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.post("/", response_model=CalendarItemResponse)
def create_calendar_item(
    item: CalendarItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    org_id = current_user["organization_id"]

    # 1️⃣ Validar Post (y que sea de la misma org)
    post = db.query(Post).filter(
        Post.id == item.post_id,
        Post.organization_id == org_id
    ).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 2️⃣ Validar Account (y que sea de la misma org)
    account = db.query(Account).filter(
        Account.id == item.account_id,
        Account.organization_id == org_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # 3️⃣ Crear CalendarItem (asignando org)
    calendar_item = CalendarItem(
        post_id=item.post_id,
        account_id=item.account_id,
        scheduled_at=to_utc_naive(item.scheduled_at),
        organization_id=org_id
    )
    db.add(calendar_item)
    db.flush()  # obtiene calendar_item.id antes del commit

    # 4️⃣ Cambiar estado del Post
    post.status = "scheduled"

    # 5️⃣ Crear Schedule automático en estado pending
    schedule = Schedule(
        calendar_item_id=calendar_item.id,
        status="pending"
    )
    db.add(schedule)

    # 6️⃣ Guardar todo
    db.commit()
    db.refresh(calendar_item)

    return calendar_item


@router.get("/")
def get_calendar_items(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    org_id = current_user["organization_id"]

    return db.query(CalendarItem).filter(
        CalendarItem.organization_id == org_id
    ).all()