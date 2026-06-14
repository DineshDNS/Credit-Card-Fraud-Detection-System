from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.admin import Admin

from app.core.security import verify_password
from app.core.auth import create_access_token

router = APIRouter()


@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    admin = (
        db.query(Admin)
        .filter(
            Admin.username == username
        )
        .first()
    )

    if not admin:

        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if not verify_password(
        password,
        admin.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = (
        create_access_token(
            data={
                "sub":
                admin.username
            },
            expires_delta=
            timedelta(hours=1)
        )
    )

    return {

        "access_token":
            access_token,

        "token_type":
            "bearer"
    }