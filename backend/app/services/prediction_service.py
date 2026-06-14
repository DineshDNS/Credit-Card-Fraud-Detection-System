import joblib
import pandas as pd

# -----------------------------
# Load Artifacts Once
# -----------------------------

model = joblib.load(
    "../artifacts/random_forest.pkl"
)

preprocessor = joblib.load(
    "../artifacts/preprocessor.pkl"
)

THRESHOLD = 0.60


def predict_transaction(transaction):

    data = pd.DataFrame([{

        "Time": transaction.time,

        "V1": transaction.v1,
        "V2": transaction.v2,
        "V3": transaction.v3,
        "V4": transaction.v4,
        "V5": transaction.v5,
        "V6": transaction.v6,
        "V7": transaction.v7,
        "V8": transaction.v8,
        "V9": transaction.v9,
        "V10": transaction.v10,
        "V11": transaction.v11,
        "V12": transaction.v12,
        "V13": transaction.v13,
        "V14": transaction.v14,
        "V15": transaction.v15,
        "V16": transaction.v16,
        "V17": transaction.v17,
        "V18": transaction.v18,
        "V19": transaction.v19,
        "V20": transaction.v20,
        "V21": transaction.v21,
        "V22": transaction.v22,
        "V23": transaction.v23,
        "V24": transaction.v24,
        "V25": transaction.v25,
        "V26": transaction.v26,
        "V27": transaction.v27,
        "V28": transaction.v28,

        "Amount": float(
            transaction.amount
        ),

        "Merchant": transaction.merchant,
        "Location": transaction.location,
        "TransactionType":
            transaction.transaction_type,

        "TransactionFrequency": 0,
        "UserAvgAmount": 0,
        "TimeGap": 0,
        "LocationDeviation": 0,
        "UnusualSpending": 0,
        "Hour": 12,
        "NightTransaction": 0,
        "HighAmountFlag":
            1 if transaction.amount > 50000 else 0,
        "RapidTransaction": 0

    }])

    X = preprocessor.transform(
        data
    )

    probability = (
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

    return {
        "fraud_probability":
            round(probability, 4),

        "prediction":
            prediction,

        "risk_level":
            risk_level
    }