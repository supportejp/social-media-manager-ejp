from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from api.models.user import User
from api.models.organization import Organization
from api.schemas.auth import LoginRequest, LoginResponse
from api.services.security import verify_password
from api.services.jwt_service import create_access_token
from api.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "organization_id": user.organization_id,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    org = db.query(Organization).filter(Organization.id == current_user["organization_id"]).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "organization_id": org.id,
        "organization_name": org.name
    }