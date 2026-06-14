import time
import joblib
import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

THRESHOLD = 0.60

STREAM_SIZE = 50

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

# ----------------------------------
# Create Demo Stream
# ----------------------------------

frauds = df[
    df["Class"] == 1
].sample(
    n=10,
    random_state=42
)

genuine = df[
    df["Class"] == 0
].sample(
    n=40,
    random_state=42
)

stream_df = pd.concat(
    [frauds, genuine]
).sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

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
# Results Storage
# ----------------------------------

results = []

# ----------------------------------
# Streaming Loop
# ----------------------------------

print("=" * 80)
print("REAL-TIME FRAUD MONITORING STARTED")
print("=" * 80)

for _, row in stream_df.iterrows():

    transaction_id = row["TransactionID"]

    actual_class = row["Class"]

    transaction = pd.DataFrame([row])

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

    X_processed = (
        preprocessor.transform(X)
    )

    probability = (
        model.predict_proba(
            X_processed
        )[0][1]
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

    # ------------------------------
    # Alert
    # ------------------------------

    if prediction == "Fraud":

        print(
            f"\nALERT: {transaction_id}"
        )

        print(
            f"Fraud Probability: "
            f"{probability:.4f}"
        )

    else:

        print(
            f"\n✓ {transaction_id}"
        )

    # ------------------------------
    # Save Result
    # ------------------------------

    results.append({

        "TransactionID":
            transaction_id,

        "ActualClass":
            actual_class,

        "FraudProbability":
            round(
                probability,
                4
            ),

        "Prediction":
            prediction,

        "RiskLevel":
            risk_level

    })

    time.sleep(1)

# ----------------------------------
# Save Results
# ----------------------------------

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "data/live/live_predictions.csv",
    index=False
)

print("\n")
print("=" * 80)

print(
    "LIVE STREAM COMPLETED"
)

print(
    f"Transactions Processed: "
    f"{len(results_df)}"
)

print(
    f"Frauds Detected: "
    f"{(results_df['Prediction'] == 'Fraud').sum()}"
)

print("=" * 80)