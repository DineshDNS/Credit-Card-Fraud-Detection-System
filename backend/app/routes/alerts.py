from fastapi import APIRouter
from fastapi import Depends

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