import pandas as pd

from app.database.connection import SessionLocal
from app.models.transaction import Transaction

db = SessionLocal()

df = pd.read_csv(
    "../data/processed/featured_creditcard.csv"
)

df["TransactionTimestamp"] = pd.to_datetime(
    df["TransactionTimestamp"]
)

count = 0

for _, row in df.iterrows():

    transaction = Transaction(

        transaction_id=row["TransactionID"],

        user_id=row["UserID"],

        merchant=row["Merchant"],

        location=row["Location"],

        transaction_type=row["TransactionType"],

        amount=float(row["Amount"]),

        transaction_time=row[
            "TransactionTimestamp"
        ],

        actual_class=int(row["Class"])

    )

    db.add(transaction)

    count += 1

    if count % 5000 == 0:

        print(
            f"Inserted {count}"
        )

db.commit()

db.close()

print(
    f"Loaded {count} transactions"
)