import pandas as pd

# ---------------------------------
# Load Dataset
# ---------------------------------

df = pd.read_csv(
    "data/processed/cleaned_creditcard.csv"
)

print("=" * 50)
print("FEATURE ENGINEERING STARTED")
print("=" * 50)

print("\nOriginal Shape:")
print(df.shape)

# ---------------------------------
# Timestamp Conversion
# ---------------------------------

df["TransactionTimestamp"] = pd.to_datetime(
    df["TransactionTimestamp"]
)

# ---------------------------------
# Sort Transactions
# ---------------------------------

df = df.sort_values(
    ["UserID", "TransactionTimestamp"]
).reset_index(drop=True)

# ---------------------------------
# Transaction Frequency
# ---------------------------------

df["TransactionFrequency"] = (
    df.groupby("UserID")["UserID"]
      .transform("count")
)

# ---------------------------------
# User Average Amount
# ---------------------------------

df["UserAvgAmount"] = (
    df.groupby("UserID")["Amount"]
      .transform("mean")
)

# ---------------------------------
# Time Gap (seconds)
# ---------------------------------

df["TimeGap"] = (
    df.groupby("UserID")["TransactionTimestamp"]
      .diff()
      .dt.total_seconds()
)

df["TimeGap"] = (
    df["TimeGap"]
      .fillna(0)
)

# ---------------------------------
# Location Deviation
# ---------------------------------

df["LocationDeviation"] = (
    df["Location"] !=
    df["HomeLocation"]
).astype(int)

# ---------------------------------
# Unusual Spending
# ---------------------------------

df["UnusualSpending"] = (
    df["Amount"] >
    (df["UserAvgAmount"] * 3)
).astype(int)

# ---------------------------------
# Hour Extraction
# ---------------------------------

df["Hour"] = (
    df["TransactionTimestamp"]
      .dt.hour
)

# ---------------------------------
# Night Transaction
# 12 AM - 5 AM
# ---------------------------------

df["NightTransaction"] = (
    (df["Hour"] >= 0) &
    (df["Hour"] <= 5)
).astype(int)

# ---------------------------------
# High Amount Flag
# ---------------------------------

df["HighAmountFlag"] = (
    df["Amount"] > 50000
).astype(int)

# ---------------------------------
# Rapid Transaction
# Less than 60 sec
# Ignore first transaction
# ---------------------------------

df["RapidTransaction"] = (
    (df["TimeGap"] > 0) &
    (df["TimeGap"] < 60)
).astype(int)

# ---------------------------------
# Validation Checks
# ---------------------------------

print("\nFeature Summary")

print(
    "\nLocationDeviation:"
)

print(
    df["LocationDeviation"]
      .value_counts()
)

print(
    "\nHighAmountFlag:"
)

print(
    df["HighAmountFlag"]
      .value_counts()
)

print(
    "\nRapidTransaction:"
)

print(
    df["RapidTransaction"]
      .value_counts()
)

# ---------------------------------
# Check Missing Values
# ---------------------------------

feature_columns = [
    "TransactionFrequency",
    "UserAvgAmount",
    "TimeGap",
    "LocationDeviation",
    "UnusualSpending",
    "NightTransaction",
    "HighAmountFlag",
    "RapidTransaction"
]

print(
    "\nFeature Missing Values:"
)

print(
    df[feature_columns]
      .isnull()
      .sum()
)

# ---------------------------------
# Save Dataset
# ---------------------------------

output_path = (
    "data/processed/featured_creditcard.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("\nFeature Dataset Saved")

print("\nFinal Shape:")
print(df.shape)

print("\nFEATURE ENGINEERING COMPLETED")