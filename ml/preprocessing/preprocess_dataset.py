import pandas as pd

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv(
    "data/processed/enhanced_creditcard.csv"
)

print("=" * 50)
print("DATA PREPROCESSING STARTED")
print("=" * 50)

print("\nOriginal Shape:")
print(df.shape)

# ----------------------------------
# Missing Values Check
# ----------------------------------

missing_values = df.isnull().sum().sum()

print("\nMissing Values:")
print(missing_values)

# ----------------------------------
# Duplicate TransactionID Check
# ----------------------------------

duplicate_txn = (
    df["TransactionID"]
    .duplicated()
    .sum()
)

print("\nDuplicate Transaction IDs:")
print(duplicate_txn)

# ----------------------------------
# Timestamp Conversion
# ----------------------------------

df["TransactionTimestamp"] = pd.to_datetime(
    df["TransactionTimestamp"]
)

print("\nTimestamp Converted")

# ----------------------------------
# Data Types
# ----------------------------------

print("\nData Types:")
print(df.dtypes.head(10))

# ----------------------------------
# Save Clean Dataset
# ----------------------------------

output_path = (
    "data/processed/cleaned_creditcard.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("\nClean Dataset Saved")

print("\nFinal Shape:")
print(df.shape)

print("\nPREPROCESSING COMPLETED")