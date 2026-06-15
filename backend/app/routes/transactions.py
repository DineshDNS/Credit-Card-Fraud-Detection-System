from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.transaction import Transaction
from app.models.fraud_prediction import FraudPrediction

router = APIRouter()


@router.get("/transactions")
def get_transactions(
    transaction_type: str = "all",
    search: str = "",
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    query = db.query(Transaction)

    if search:

        query = query.filter(
            Transaction.transaction_id.ilike(
                f"%{search}%"
            )
        )

    transactions = query.all()

    results = []

    for txn in transactions:

        prediction = (
            db.query(FraudPrediction)
            .filter(
                FraudPrediction.transaction_id
                == txn.transaction_id
            )
            .first()
        )

        status = "Legitimate"
        risk_level = "Low"

        if prediction:

            status = prediction.prediction
            risk_level = prediction.risk_level

        if (
            transaction_type == "fraud"
            and status != "Fraud"
        ):
            continue

        if (
            transaction_type == "genuine"
            and status != "Legitimate"
        ):
            continue

        results.append({

            "transaction_id":
                txn.transaction_id,

            "user_id":
                txn.user_id,

            "merchant":
                txn.merchant,

            "location":
                txn.location,

            "amount":
                float(txn.amount),

            "transaction_time":
                txn.transaction_time,

            "prediction":
                status,

            "risk_level":
                risk_level
        })

    total_records = len(results)

    start = (
        (page - 1)
        * page_size
    )

    end = start + page_size

    paginated = results[start:end]

    return {

        "page":
            page,

        "page_size":
            page_size,

        "total_records":
            total_records,

        "total_pages":
            (
                total_records
                +
                page_size
                -
                1
            )
            // page_size,

        "transactions":
            paginated
    }


@router.get("/transactions/summary")
def get_transaction_summary(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    total = (
        db.query(Transaction)
        .count()
    )

    fraud = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.prediction
            == "Fraud"
        )
        .count()
    )

    genuine = (
        total - fraud
    )

    return {

        "total_transactions":
            total,

        "fraud_transactions":
            fraud,

        "genuine_transactions":
            genuine
    }