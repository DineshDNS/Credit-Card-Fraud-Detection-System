import pandas as pd

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

# ----------------------------------
# Business Risk Score
# ----------------------------------

df["RiskScore"] = (

    df["HighAmountFlag"] +

    df["LocationDeviation"] +

    df["UnusualSpending"] +

    df["RapidTransaction"] +

    df["NightTransaction"]

)

# ----------------------------------
# Business Fraud Label
# ----------------------------------

df["BusinessFraudLabel"] = (
    df["RiskScore"] >= 3
).astype(int)

# ----------------------------------
# Save
# ----------------------------------

df.to_csv(
    "data/processed/business_featured_creditcard.csv",
    index=False
)

print("=" * 50)

print(
    df["BusinessFraudLabel"]
      .value_counts()
)

print("\nFraud Percentage:")

print(
    round(
        df["BusinessFraudLabel"]
          .mean() * 100,
        2
    ),
    "%"
)