from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal
from api.models.organization import Organization

router = APIRouter(prefix="/organizations", tags=["Organizations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_organization(name: str, db: Session = Depends(get_db)):

    org = Organization(name=name)
    db.add(org)
    db.commit()
    db.refresh(org)

    return org


@router.get("/")
def get_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()