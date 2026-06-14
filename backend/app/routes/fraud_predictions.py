from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.fraud_prediction import FraudPrediction

router = APIRouter()


@router.get("/fraud-predictions")
def get_predictions(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    return (
        db.query(FraudPrediction)
        .all()
    )