import pandas as pd

df = pd.read_csv(
    "data/processed/featured_creditcard.csv"
)

print("=" * 50)

print("Shape:")
print(df.shape)

print("\nFeature Summary")

features = [
    "TransactionFrequency",
    "UserAvgAmount",
    "TimeGap",
    "LocationDeviation",
    "UnusualSpending",
    "NightTransaction",
    "HighAmountFlag",
    "RapidTransaction"
]

for feature in features:

    print(f"\n{feature}")

    print(
        df[feature]
          .describe()
    )

print("\nMissing Values")

print(
    df[features]
      .isnull()
      .sum()
)