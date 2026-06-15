import joblib
import pandas as pd

from app.models.fraud_prediction import FraudPrediction
from app.services.alert_service import create_alert
from app.services.production_feature_service import (
    build_features
)

from app.models.customer import Customer

from app.services.notification_service import (
    send_email_alert,
    send_sms_alert
)
# -------------------------
# Load Once
# -------------------------

model = joblib.load(
    "../artifacts/business_random_forest.pkl"
)

preprocessor = joblib.load(
    "../artifacts/business_preprocessor.pkl"
)

THRESHOLD = 0.80


def predict_transaction(
    db,
    transaction
):

    features = build_features(
        db,
        transaction
    )

    feature_df = pd.DataFrame(
        [features]
    )

    X = preprocessor.transform(
        feature_df
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
            == transaction.transaction_id
        )
        .first()
    )

    if not existing:

        record = FraudPrediction(

            transaction_id=
                transaction.transaction_id,

            fraud_probability=
                round(probability, 4),

            prediction=
                prediction,

            risk_level=
                risk_level
        )

        db.add(record)

        db.commit()

    create_alert(
        db,
        transaction.transaction_id,
        risk_level,
        prediction
    )

    if prediction == "Fraud":

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id
                == transaction.user_id
            )
            .first()
        )

        if customer:

            send_email_alert(
                customer,
                transaction,
                prediction,
                risk_level
            )

            send_sms_alert(
                customer,
                transaction,
                prediction
            )

            print(
                f"SMS SENT TO "
                f"{customer.phone}"
                 )

    return {
        "transaction_id":
            transaction.transaction_id,

        "fraud_probability":
            round(probability, 4),

        "prediction":
            prediction,

        "risk_level":
            risk_level
    }