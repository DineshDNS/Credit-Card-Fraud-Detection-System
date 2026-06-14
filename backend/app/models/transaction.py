from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import Integer
from sqlalchemy import DateTime

from app.database.base import Base


class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        String(20),
        primary_key=True
    )

    user_id = Column(
        String(20)
    )

    merchant = Column(
        String(100)
    )

    location = Column(
        String(100)
    )

    transaction_type = Column(
        String(20)
    )

    amount = Column(
        Numeric(12, 2)
    )

    transaction_time = Column(
        DateTime
    )

    actual_class = Column(
        Integer
    )