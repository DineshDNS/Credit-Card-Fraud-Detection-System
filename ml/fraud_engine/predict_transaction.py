import joblib
import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

TRANSACTION_ID = "TXN0081610"

THRESHOLD = 0.60

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

# ----------------------------------
# Find Transaction
# ----------------------------------

transaction = df[
    df["TransactionID"] == TRANSACTION_ID
]

if len(transaction) == 0:

    raise ValueError(
        f"{TRANSACTION_ID} not found"
    )

# ----------------------------------
# Save Actual Label
# ----------------------------------

actual_class = int(
    transaction["Class"].iloc[0]
)

# ----------------------------------
# Prepare Features
# ----------------------------------

drop_columns = [
    "Class",
    "TransactionID",
    "UserID",
    "CustomerName",
    "CustomerEmail",
    "CustomerPhone",
    "HomeLocation",
    "TransactionTimestamp"
]

X = transaction.drop(
    columns=drop_columns
)

# ----------------------------------
# Load Artifacts
# ----------------------------------

preprocessor = joblib.load(
    "artifacts/preprocessor.pkl"
)

model = joblib.load(
    "artifacts/random_forest.pkl"
)

# ----------------------------------
# Transform
# ----------------------------------

X_processed = preprocessor.transform(
    X
)

# ----------------------------------
# Predict
# ----------------------------------

fraud_probability = (
    model.predict_proba(
        X_processed
    )[0][1]
)

prediction = (
    "Fraud"
    if fraud_probability >= THRESHOLD
    else "Legitimate"
)

# ----------------------------------
# Risk Level
# ----------------------------------

if fraud_probability >= 0.80:

    risk_level = "High"

elif fraud_probability >= 0.60:

    risk_level = "Medium"

else:

    risk_level = "Low"

# ----------------------------------
# Results
# ----------------------------------

print("=" * 50)

print(
    f"Transaction ID: {TRANSACTION_ID}"
)

print(
    f"Actual Class: {actual_class}"
)

print(
    f"Fraud Probability: "
    f"{fraud_probability:.4f}"
)

print(
    f"Prediction: {prediction}"
)

print(
    f"Risk Level: {risk_level}"
)