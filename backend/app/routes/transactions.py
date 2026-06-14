from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.transaction import Transaction

router = APIRouter()


@router.get("/transactions")
def get_transactions(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):

    transactions = (
        db.query(Transaction)
        .limit(limit)
        .all()
    )

    return transactions