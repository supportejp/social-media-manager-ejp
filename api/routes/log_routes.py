from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.models.log import Log
from api.schemas.log import LogResponse
from api.core.dependencies import get_db
from api.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/")
def get_logs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    org_id = current_user["organization_id"]

    return db.query(Log).filter(
        Log.organization_id == org_id
    ).order_by(Log.created_at.desc()).all()