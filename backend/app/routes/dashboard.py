from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.transaction import Transaction

router = APIRouter()


@router.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):

    total_transactions = (
        db.query(Transaction)
        .count()
    )

    fraud_count = (
        db.query(Transaction)
        .filter(
            Transaction.actual_class == 1
        )
        .count()
    )

    fraud_rate = round(
        fraud_count /
        total_transactions * 100,
        2
    )

    return {

        "total_transactions":
            total_transactions,

        "fraud_count":
            fraud_count,

        "fraud_rate":
            fraud_rate
    }