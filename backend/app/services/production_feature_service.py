from datetime import datetime

from app.models.transaction import Transaction
from app.models.customer import Customer


def build_features(
    db,
    transaction
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id
            == transaction.user_id
        )
        .first()
    )

    user_transactions = (
        db.query(Transaction)
        .filter(
            Transaction.user_id
            == transaction.user_id
        )
        .all()
    )

    transaction_frequency = (
        len(user_transactions)
    )

    avg_amount = (
        sum(
            float(t.amount)
            for t in user_transactions
        )
        /
        max(
            transaction_frequency,
            1
        )
    )

    previous_transactions = sorted(
        user_transactions,
        key=lambda x:
        x.transaction_time
    )

    time_gap = 0

    if len(previous_transactions) > 1:

        last_txn = (
            previous_transactions[-2]
        )

        time_gap = (
            transaction.transaction_time
            -
            last_txn.transaction_time
        ).total_seconds()

    location_deviation = int(

        customer
        and

        transaction.location
        !=
        customer.home_location
    )

    unusual_spending = int(
        float(transaction.amount)
        >
        (avg_amount * 3)
    )

    hour = (
        transaction.transaction_time.hour
    )

    night_transaction = int(
        0 <= hour <= 5
    )

    high_amount_flag = int(
        float(transaction.amount)
        > 50000
    )

    rapid_transaction = int(
        0 < time_gap < 60
    )

    return {

        "Amount":
            float(transaction.amount),

        "Merchant":
            transaction.merchant,

        "Location":
            transaction.location,

        "TransactionType":
            transaction.transaction_type,

        "TransactionFrequency":
            transaction_frequency,

        "UserAvgAmount":
            avg_amount,

        "TimeGap":
            time_gap,

        "LocationDeviation":
            location_deviation,

        "UnusualSpending":
            unusual_spending,

        "Hour":
            hour,

        "NightTransaction":
            night_transaction,

        "HighAmountFlag":
            high_amount_flag,

        "RapidTransaction":
            rapid_transaction
    }