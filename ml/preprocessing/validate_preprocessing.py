import pandas as pd

df = pd.read_csv(
    "data/processed/cleaned_creditcard.csv"
)

print("=" * 50)

print("Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Transaction IDs:")
print(
    df["TransactionID"]
      .duplicated()
      .sum()
)

df["TransactionTimestamp"] = pd.to_datetime(
    df["TransactionTimestamp"]
)

print("\nTimestamp Dtype:")
print(
    df["TransactionTimestamp"].dtype
)

print("\nSample Rows:")

print(
    df[
        [
            "TransactionID",
            "UserID",
            "Merchant",
            "Location",
            "TransactionTimestamp"
        ]
    ].head()
)