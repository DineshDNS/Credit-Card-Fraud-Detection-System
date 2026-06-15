import pandas as pd

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.customer import Customer
from app.models.transaction import Transaction

from app.services.production_prediction_service import (
    predict_transaction
)

from datetime import datetime

from app.models.upload_history import (
    UploadHistory
)

from app.models.fraud_prediction import (
    FraudPrediction
)

router = APIRouter()


@router.post("/upload-transactions")
def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    try:

        if file.filename.endswith(".csv"):

            df = pd.read_csv(
                file.file
            )

        elif file.filename.endswith(
            ".xlsx"
        ):

            df = pd.read_excel(
                file.file
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Only CSV/XLSX files are allowed"
            )

        required_columns = [

            "transaction_id",
            "customer_id",
            "customer_name",
            "email",
            "phone",
            "amount",
            "merchant",
            "location",
            "transaction_type",
            "transaction_time"
        ]

        for column in required_columns:

            if column not in df.columns:

                raise HTTPException(
                    status_code=400,
                    detail=f"Missing column: {column}"
                )

        inserted_customers = 0
        inserted_transactions = 0

        processed_customers = set()
        processed_transactions = set()

        newly_inserted_transactions = []

        for _, row in df.iterrows():

            customer_id = str(
                row["customer_id"]
            )

            transaction_id = str(
                row["transaction_id"]
            )

            # -------------------------
            # Customer Insert
            # -------------------------

            if customer_id not in processed_customers:

                existing_customer = (
                    db.query(Customer)
                    .filter(
                        Customer.customer_id
                        == customer_id
                    )
                    .first()
                )

                if not existing_customer:

                    customer = Customer(

                        customer_id=
                            customer_id,

                        customer_name=
                            row[
                                "customer_name"
                            ],

                        email=
                            row[
                                "email"
                            ],

                        phone=
                            str(
                                row[
                                    "phone"
                                ]
                            ),

                        home_location=
                            row[
                                "location"
                            ]
                    )

                    db.add(customer)

                    inserted_customers += 1

                processed_customers.add(
                    customer_id
                )

            # -------------------------
            # Transaction Insert
            # -------------------------

            if transaction_id not in processed_transactions:

                existing_txn = (
                    db.query(Transaction)
                    .filter(
                        Transaction.transaction_id
                        == transaction_id
                    )
                    .first()
                )

                if not existing_txn:

                    transaction = Transaction(

                        transaction_id=
                            transaction_id,

                        user_id=
                            customer_id,

                        merchant=
                            row[
                                "merchant"
                            ],

                        location=
                            row[
                                "location"
                            ],

                        transaction_type=
                            row[
                                "transaction_type"
                            ],

                        amount=
                            row[
                                "amount"
                            ],

                        transaction_time=
                            pd.to_datetime(
                                row[
                                    "transaction_time"
                                ]
                            ),

                        actual_class=0
                    )

                    db.add(transaction)

                    newly_inserted_transactions.append(
                        transaction
                    )

                    inserted_transactions += 1

                processed_transactions.add(
                    transaction_id
                )

        db.commit()

        # -------------------------
        # Auto Prediction
        # -------------------------

        predictions_created = 0

        for txn in newly_inserted_transactions:

            predict_transaction(
                db,
                txn
            )

            predictions_created += 1


        # -------------------------
        # Fraud Count
        # -------------------------

        fraud_detected = (

            db.query(
                FraudPrediction
            )

            .filter(
                FraudPrediction.prediction
                == "Fraud"
            )

            .filter(
                FraudPrediction.transaction_id.in_(
                    [
                        txn.transaction_id
                        for txn
                        in newly_inserted_transactions
                    ]
                )
            )

            .count()

        )

        # -------------------------
        # Upload History Save
        # -------------------------

        history = UploadHistory(

            file_name=
                file.filename,

            records_count=
                inserted_transactions,

            fraud_detected=
                fraud_detected,

            uploaded_at=
                datetime.utcnow()

        )

        db.add(history)

        db.commit()

        return {

            "customers_inserted":
                inserted_customers,

            "transactions_inserted":
                inserted_transactions,

            "predictions_created":
                predictions_created,

            "fraud_detected":
                fraud_detected,

            "uploaded_file":
                file.filename
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )