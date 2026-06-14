from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from app.database.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    alert_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_id = Column(
        String(20),
        ForeignKey(
            "transactions.transaction_id"
        )
    )

    alert_type = Column(
        String(20)
    )

    alert_status = Column(
        String(20)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )