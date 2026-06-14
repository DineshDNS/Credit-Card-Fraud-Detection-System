import pandas as pd

df = pd.read_csv(
    "data/processed/enhanced_creditcard.csv"
)

print("=" * 50)

print("Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Transaction IDs:")
print(
    df["TransactionID"].duplicated().sum()
)

print("\nUnique Users:")
print(
    df["UserID"].nunique()
)

print("\nTransaction Types:")
print(
    df["TransactionType"].value_counts()
)

print("\nFraud Distribution:")
print(
    df["Class"].value_counts()
)

print("\nSample Columns:")
print(
    df[[
        "TransactionID",
        "UserID",
        "Merchant",
        "Location",
        "TransactionType",
        "TransactionTimestamp"
    ]].head()
)