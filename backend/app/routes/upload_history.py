from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_admin

from app.models.upload_history import (
    UploadHistory
)

router = APIRouter()


@router.get("/upload-history")
def get_upload_history(

    db: Session = Depends(get_db),

    current_admin: str = Depends(
        get_current_admin
    )

):

    history = (

        db.query(
            UploadHistory
        )

        .order_by(
            UploadHistory.uploaded_at.desc()
        )

        .all()

    )

    return history