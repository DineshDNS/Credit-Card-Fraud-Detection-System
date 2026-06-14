import pandas as pd
from datetime import datetime


def build_features(
    user_id,
    amount,
    merchant,
    location,
    transaction_type
):
    """
    Build model features for a new transaction
    """

    history = pd.read_csv(
        "data/processed/featured_creditcard.csv"
    )

    customer_master = pd.read_csv(
        "data/processed/customers.csv"
    )

    user_history = history[
        history["UserID"] == user_id
    ]

    if len(user_history) == 0:
        raise ValueError(
            f"User {user_id} not found"
        )

    customer = customer_master[
        customer_master["UserID"] == user_id
    ]

    home_location = (
        customer["HomeLocation"]
        .iloc[0]
    )

    current_time = datetime.now()

    # --------------------------------
    # Transaction Frequency
    # --------------------------------

    transaction_frequency = len(
        user_history
    ) + 1

    # --------------------------------
    # User Average Amount
    # --------------------------------

    user_avg_amount = (
        user_history["Amount"]
        .mean()
    )

    # --------------------------------
    # Time Gap
    # --------------------------------

    last_transaction_time = pd.to_datetime(
        user_history[
            "TransactionTimestamp"
        ]
    ).max()

    time_gap = (
        current_time -
        last_transaction_time
    ).total_seconds()

    # --------------------------------
    # Location Deviation
    # --------------------------------

    location_deviation = int(
        location != home_location
    )

    # --------------------------------
    # Unusual Spending
    # --------------------------------

    unusual_spending = int(
        amount >
        (user_avg_amount * 3)
    )

    # --------------------------------
    # Hour
    # --------------------------------

    hour = current_time.hour

    # --------------------------------
    # Night Transaction
    # --------------------------------

    night_transaction = int(
        0 <= hour <= 5
    )

    # --------------------------------
    # High Amount
    # --------------------------------

    high_amount_flag = int(
        amount > 50000
    )

    # --------------------------------
    # Rapid Transaction
    # --------------------------------

    rapid_transaction = int(
        0 < time_gap < 60
    )

    return {

        "Merchant": merchant,
        "Location": location,
        "TransactionType": transaction_type,

        "Amount": amount,

        "TransactionFrequency":
            transaction_frequency,

        "UserAvgAmount":
            user_avg_amount,

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