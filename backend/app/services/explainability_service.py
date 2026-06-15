def generate_explanation(
    features
):

    reasons = []

    if features["HighAmountFlag"] == 1:

        reasons.append(
            "High Amount Transaction"
        )

    if features["LocationDeviation"] == 1:

        reasons.append(
            "Location Deviation Detected"
        )

    if features["NightTransaction"] == 1:

        reasons.append(
            "Night Time Transaction"
        )

    if features["RapidTransaction"] == 1:

        reasons.append(
            "Rapid Consecutive Transactions"
        )

    if features["UnusualSpending"] == 1:

        reasons.append(
            "Unusual Spending Pattern"
        )

    if len(reasons) == 0:

        reasons.append(
            "Normal Customer Behaviour"
        )

    return reasons