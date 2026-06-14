from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.alert import Alert

router = APIRouter()


@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    return (
        db.query(Alert)
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )


@router.put("/alerts/{alert_id}")
def update_alert_status(
    alert_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.alert_id == alert_id
        )
        .first()
    )

    if not alert:

        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.alert_status = status

    db.commit()

    db.refresh(alert)

    return alert