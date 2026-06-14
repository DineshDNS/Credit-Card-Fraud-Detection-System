import pandas as pd

df = pd.read_csv(
    "data/processed/enhanced_creditcard.csv"
)

customers = (
    df[
        [
            "UserID",
            "CustomerName",
            "CustomerEmail",
            "CustomerPhone",
            "HomeLocation"
        ]
    ]
    .drop_duplicates(subset=["UserID"])
)

customers.to_csv(
    "data/processed/customers.csv",
    index=False
)

print(customers.shape)
print("Customer Master Created")