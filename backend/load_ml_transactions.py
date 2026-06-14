import pandas as pd

from app.database.connection import SessionLocal
from app.models.ml_transaction import MLTransaction

db = SessionLocal()

print("Loading CSV...")

df = pd.read_csv(
    "../data/processed/featured_creditcard.csv"
)

print(df.shape)

records = []

for _, row in df.iterrows():

    records.append(

        MLTransaction(

            transaction_id=row["TransactionID"],

            Time=row["Time"],

            V1=row["V1"],
            V2=row["V2"],
            V3=row["V3"],
            V4=row["V4"],
            V5=row["V5"],
            V6=row["V6"],
            V7=row["V7"],
            V8=row["V8"],
            V9=row["V9"],
            V10=row["V10"],
            V11=row["V11"],
            V12=row["V12"],
            V13=row["V13"],
            V14=row["V14"],
            V15=row["V15"],
            V16=row["V16"],
            V17=row["V17"],
            V18=row["V18"],
            V19=row["V19"],
            V20=row["V20"],
            V21=row["V21"],
            V22=row["V22"],
            V23=row["V23"],
            V24=row["V24"],
            V25=row["V25"],
            V26=row["V26"],
            V27=row["V27"],
            V28=row["V28"],

            Amount=row["Amount"],

            Merchant=row["Merchant"],

            Location=row["Location"],

            TransactionType=row["TransactionType"],

            TransactionFrequency=row[
                "TransactionFrequency"
            ],

            UserAvgAmount=row[
                "UserAvgAmount"
            ],

            TimeGap=row[
                "TimeGap"
            ],

            LocationDeviation=row[
                "LocationDeviation"
            ],

            UnusualSpending=row[
                "UnusualSpending"
            ],

            Hour=row["Hour"],

            NightTransaction=row[
                "NightTransaction"
            ],

            HighAmountFlag=row[
                "HighAmountFlag"
            ],

            RapidTransaction=row[
                "RapidTransaction"
            ]
        )
    )

    if len(records) == 5000:

        db.bulk_save_objects(
            records
        )

        db.commit()

        print(
            "Inserted 5000"
        )

        records = []

if records:

    db.bulk_save_objects(
        records
    )

    db.commit()

db.close()

print(
    "ML Transactions Loaded"
)