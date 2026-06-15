from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.fraud_prediction import (
    FraudPrediction
)

router = APIRouter()


@router.get("/fraud-predictions")
def get_predictions(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    predictions = (

        db.query(
            FraudPrediction
        )

        .order_by(
            FraudPrediction.predicted_at.desc()
        )

        .all()

    )

    return [

        {

            "prediction_id":
                prediction.prediction_id,

            "transaction_id":
                prediction.transaction_id,

            "prediction":
                prediction.prediction,

            "risk_level":
                prediction.risk_level,

            "fraud_probability":
                prediction.fraud_probability,

            "predicted_at":
                prediction.predicted_at,

            "explanation":
                prediction.explanation

        }

        for prediction in predictions

    ]