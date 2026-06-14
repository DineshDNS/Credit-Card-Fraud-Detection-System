from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.transaction import Transaction

router = APIRouter()


@router.get("/transactions")
def get_transactions(
    transaction_type: str = "all",
    search: str = "",
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):

    query = db.query(Transaction)

    if transaction_type == "fraud":

        query = query.filter(
            Transaction.actual_class == 1
        )

    elif transaction_type == "genuine":

        query = query.filter(
            Transaction.actual_class == 0
        )

    if search:

        query = query.filter(
            Transaction.transaction_id.ilike(
                f"%{search}%"
            )
        )

    total_records = query.count()

    offset = (
        (page - 1)
        * page_size
    )

    transactions = (
        query
        .order_by(
            Transaction.transaction_time.desc()
        )
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_records,
        "total_pages": (
            total_records + page_size - 1
        ) // page_size,
        "transactions": transactions
    }


@router.get("/transactions/summary")
def get_transaction_summary(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):

    total = (
        db.query(Transaction)
        .count()
    )

    fraud = (
        db.query(Transaction)
        .filter(
            Transaction.actual_class == 1
        )
        .count()
    )

    genuine = (
        db.query(Transaction)
        .filter(
            Transaction.actual_class == 0
        )
        .count()
    )

    return {
        "total_transactions": total,
        "fraud_transactions": fraud,
        "genuine_transactions": genuine
    }