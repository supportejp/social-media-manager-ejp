from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from api.models.schedule import Schedule
from api.models.calendar_item import CalendarItem
from api.models.post import Post
from api.models.log import Log
from api.schemas.schedule import ScheduleResponse
from api.core.dependencies import get_db
from shared.time_utils import utc_now_naive
from api.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.get("/")
def get_schedules(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    org_id = current_user["organization_id"]

    return (
        db.query(Schedule)
        .join(CalendarItem, Schedule.calendar_item_id == CalendarItem.id)
        .filter(CalendarItem.organization_id == org_id)
        .all()
    )


@router.post("/{schedule_id}/execute", response_model=ScheduleResponse)
def execute_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if schedule.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending schedules can be executed")

    # Obtener calendar_item asociado
    cal = db.query(CalendarItem).filter(CalendarItem.id == schedule.calendar_item_id).first()
    if not cal:
        raise HTTPException(status_code=404, detail="Calendar item not found")

    post = db.query(Post).filter(Post.id == cal.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # ✅ Ejecución simulada exitosa
    schedule.status = "executed"
    schedule.executed_at = utc_now_naive()

    # Cambiar estado del post a published
    post.status = "published"

    # Crear log
    log = Log(
        level="info",
        event="schedule_executed",
        message="Schedule executed successfully (simulated).",
        schedule_id=schedule.id,
        calendar_item_id=cal.id,
        post_id=post.id,
        account_id=cal.account_id
    )
    db.add(log)

    db.commit()
    db.refresh(schedule)
    return schedule