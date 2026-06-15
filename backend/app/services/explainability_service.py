def generate_explanation(
    features
):

    reasons = []

    if (
        features.get(
            "HighAmountFlag",
            0
        ) == 1
    ):

        reasons.append(
            "High Amount Transaction"
        )

    if (
        features.get(
            "LocationDeviation",
            0
        ) == 1
    ):

        reasons.append(
            "Location Deviation Detected"
        )

    if (
        features.get(
            "NightTransaction",
            0
        ) == 1
    ):

        reasons.append(
            "Night Time Transaction"
        )

    if (
        features.get(
            "RapidTransaction",
            0
        ) == 1
    ):

        reasons.append(
            "Rapid Consecutive Transactions"
        )

    if (
        features.get(
            "UnusualSpending",
            0
        ) == 1
    ):

        reasons.append(
            "Unusual Spending Pattern"
        )

    if (
        features.get(
            "TransactionFrequency",
            0
        ) > 10
    ):

        reasons.append(
            "Abnormally High Transaction Frequency"
        )

    if (
        features.get(
            "TimeGap",
            9999
        ) < 5
    ):

        reasons.append(
            "Very Short Gap Between Transactions"
        )

    if len(reasons) == 0:

        reasons.append(
            "Normal Customer Behaviour"
        )

    return reasons