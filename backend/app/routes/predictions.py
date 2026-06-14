import joblib
import pandas as pd

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.ml_transaction import MLTransaction
from app.models.fraud_prediction import FraudPrediction
from app.services.alert_service import (
    create_alert
)

router = APIRouter()

# ---------------------------------
# Load Once
# ---------------------------------

model = joblib.load(
    "../artifacts/random_forest.pkl"
)

preprocessor = joblib.load(
    "../artifacts/preprocessor.pkl"
)

THRESHOLD = 0.60


@router.post("/predict/{transaction_id}")
def predict_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    transaction = (
        db.query(MLTransaction)
        .filter(
            MLTransaction.transaction_id
            == transaction_id
        )
        .first()
    )

    if not transaction:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    feature_data = pd.DataFrame([{

        "Time": transaction.Time,

        "V1": transaction.V1,
        "V2": transaction.V2,
        "V3": transaction.V3,
        "V4": transaction.V4,
        "V5": transaction.V5,
        "V6": transaction.V6,
        "V7": transaction.V7,
        "V8": transaction.V8,
        "V9": transaction.V9,
        "V10": transaction.V10,
        "V11": transaction.V11,
        "V12": transaction.V12,
        "V13": transaction.V13,
        "V14": transaction.V14,
        "V15": transaction.V15,
        "V16": transaction.V16,
        "V17": transaction.V17,
        "V18": transaction.V18,
        "V19": transaction.V19,
        "V20": transaction.V20,
        "V21": transaction.V21,
        "V22": transaction.V22,
        "V23": transaction.V23,
        "V24": transaction.V24,
        "V25": transaction.V25,
        "V26": transaction.V26,
        "V27": transaction.V27,
        "V28": transaction.V28,

        "Amount": transaction.Amount,

        "Merchant": transaction.Merchant,
        "Location": transaction.Location,
        "TransactionType":
            transaction.TransactionType,

        "TransactionFrequency":
            transaction.TransactionFrequency,

        "UserAvgAmount":
            transaction.UserAvgAmount,

        "TimeGap":
            transaction.TimeGap,

        "LocationDeviation":
            transaction.LocationDeviation,

        "UnusualSpending":
            transaction.UnusualSpending,

        "Hour":
            transaction.Hour,

        "NightTransaction":
            transaction.NightTransaction,

        "HighAmountFlag":
            transaction.HighAmountFlag,

        "RapidTransaction":
            transaction.RapidTransaction
    }])

    X = preprocessor.transform(
        feature_data
    )

    probability = float(
        model.predict_proba(X)[0][1]
    )

    prediction = (
        "Fraud"
        if probability >= THRESHOLD
        else "Legitimate"
    )

    if probability >= 0.80:
        risk_level = "High"
    elif probability >= 0.60:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    existing = (
        db.query(FraudPrediction)
        .filter(
            FraudPrediction.transaction_id
            == transaction_id
        )
        .first()
    )

    if not existing:

        record = FraudPrediction(

            transaction_id=transaction_id,

            fraud_probability=float(
                round(probability, 4)
            ),

            prediction=prediction,

            risk_level=risk_level
        )

        db.add(record)

        db.commit()

    create_alert(
        db,
        transaction_id,
        risk_level,
        prediction
    )

    return {
        "transaction_id":
            transaction_id,

        "fraud_probability":
            round(probability, 4),

        "prediction":
            prediction,

        "risk_level":
            risk_level
    }