from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    alert_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_id = Column(
        String(20)
    )

    alert_type = Column(
        String(50)
    )

    risk_level = Column(
        String(20)
    )

    message = Column(
        String(255)
    )

    alert_status = Column(
        String(50),
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )