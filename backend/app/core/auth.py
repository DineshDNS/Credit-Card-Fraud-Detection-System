from datetime import datetime
from datetime import timedelta

from jose import jwt
from jose import JWTError

import os

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM"
)

def create_access_token(
    data: dict,
    expires_delta=None
):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        +
        (
            expires_delta
            or timedelta(hours=1)
        )
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )