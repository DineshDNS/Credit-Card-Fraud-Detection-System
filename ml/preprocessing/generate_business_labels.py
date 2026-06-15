import pandas as pd

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

print("=" * 50)
print("GENERATING BUSINESS FRAUD LABELS")
print("=" * 50)

# ----------------------------------
# Risk Score
# ----------------------------------

risk_score = pd.Series(
    0,
    index=df.index
)

# High Amount

risk_score += (
    df["HighAmountFlag"] * 30
)

# Location Change

risk_score += (
    df["LocationDeviation"] * 25
)

# Rapid Transaction

risk_score += (
    df["RapidTransaction"] * 25
)

# Night Transaction

risk_score += (
    df["NightTransaction"] * 10
)

# Unusual Spending

risk_score += (
    df["UnusualSpending"] * 20
)

# Frequent User Activity

risk_score += (
    (
        df["TransactionFrequency"] > 20
    ).astype(int)
    * 10
)

# Very Small Time Gap

risk_score += (
    (
        df["TimeGap"] < 60
    ).astype(int)
    * 15
)

# ----------------------------------
# Save Risk Score
# ----------------------------------

df["RiskScore"] = risk_score

# ----------------------------------
# Fraud Label
# ----------------------------------

df["BusinessClass"] = (
    df["RiskScore"] >= 50
).astype(int)

# ----------------------------------
# Statistics
# ----------------------------------

print("\nBusinessClass Distribution")

print(
    df["BusinessClass"]
    .value_counts()
)

fraud_rate = (
    df["BusinessClass"]
    .mean()
    * 100
)

print(
    f"\nFraud Rate: "
    f"{fraud_rate:.2f}%"
)

# ----------------------------------
# Save
# ----------------------------------

df.to_csv(
    "data/processed/business_fraud_dataset.csv",
    index=False
)

print(
    "\nSaved:"
)

print(
    "data/processed/business_fraud_dataset.csv"
)