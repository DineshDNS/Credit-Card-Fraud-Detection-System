from app.models.alert import Alert


def create_alert(
    db,
    transaction_id,
    risk_level,
    prediction
):

    if (
        prediction != "Fraud"
        and
        risk_level != "High"
    ):
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

    alert = Alert(

        transaction_id=transaction_id,

        alert_type="Fraud",

        alert_status="Pending"
    )

    db.add(alert)

    db.commit()