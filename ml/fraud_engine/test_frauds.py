import pandas as pd

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

frauds = df[
    df["Class"] == 1
]

print(
    frauds[
        ["TransactionID", "Class"]
    ].head(20)
)