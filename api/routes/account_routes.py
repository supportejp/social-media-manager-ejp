from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.models.account import Account
from api.schemas.account import AccountCreate, AccountResponse
from api.core.dependencies import get_db
from api.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/")
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    org_id = current_user["organization_id"]

    db_account = Account(
        **account.dict(),
        organization_id=org_id
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


@router.get("/")
def get_accounts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    org_id = current_user["organization_id"]

    return db.query(Account).filter(
        Account.organization_id == org_id
    ).all()