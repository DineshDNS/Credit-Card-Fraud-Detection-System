from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.transaction import Transaction
from app.models.fraud_prediction import FraudPrediction

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
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.prediction == "Fraud"
        )
        .count()
    )

    fraud_rate = 0

    if total_transactions > 0:

        fraud_rate = round(
            (
                fraud_count /
                total_transactions
            ) * 100,
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


@router.get("/dashboard/risk-distribution")
def get_risk_distribution(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    low = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.risk_level == "Low"
        )
        .count()
    )

    medium = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.risk_level == "Medium"
        )
        .count()
    )

    high = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.risk_level == "High"
        )
        .count()
    )

    return {
        "low": low,
        "medium": medium,
        "high": high
    }


@router.get("/dashboard/fraud-trends")
def get_fraud_trends(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    trends = (

        db.query(

            func.date(
                FraudPrediction.predicted_at
            ).label("date"),

            func.count(
                FraudPrediction.prediction_id
            ).label("count")

        )

        .filter(
            FraudPrediction.prediction == "Fraud"
        )

        .group_by(
            func.date(
                FraudPrediction.predicted_at
            )
        )

        .order_by(
            func.date(
                FraudPrediction.predicted_at
            )
        )

        .all()

    )

    return [

        {
            "date": str(row.date),
            "count": row.count
        }

        for row in trends

    ]

@router.get("/dashboard/advanced-stats")
def advanced_stats(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    high_risk = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.risk_level == "High"
        )
        .count()
    )

    medium_risk = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.risk_level == "Medium"
        )
        .count()
    )

    email_alerts = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.prediction == "Fraud"
        )
        .count()
    )

    return {
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "email_alerts": email_alerts
    }


@router.get("/dashboard/recent-alerts")
def recent_alerts(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    alerts = (

        db.query(FraudPrediction)

        .filter(
            FraudPrediction.prediction
            == "Fraud"
        )

        .order_by(
            FraudPrediction.predicted_at.desc()
        )

        .limit(5)

        .all()
    )

    return [

        {
            "transaction_id":
                alert.transaction_id,

            "risk_level":
                alert.risk_level,

            "predicted_at":
                alert.predicted_at
        }

        for alert in alerts

    ]