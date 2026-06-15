from app.models.alert import Alert


def create_alert(
    db,
    transaction_id,
    risk_level,
    prediction
):

    if prediction != "Fraud":
        return

    existing = (
        db.query(Alert)
        .filter(
            Alert.transaction_id
            == transaction_id
        )
        .first()
    )

    if existing:
        return

    # Alert Message

    if risk_level == "High":

        message = (
            "High Value Transaction Detected"
        )

    elif risk_level == "Medium":

        message = (
            "Suspicious Activity Detected"
        )

    else:

        message = (
            "Unusual Transaction Pattern"
        )

    alert = Alert(

        transaction_id=
            transaction_id,

        alert_type=
            prediction,

        risk_level=
            risk_level,

        message=
            message,

        alert_status=
            "Pending"
    )

    db.add(alert)

    db.commit()