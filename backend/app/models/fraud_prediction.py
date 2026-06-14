from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from app.database.base import Base


class FraudPrediction(Base):

    __tablename__ = "fraud_predictions"

    prediction_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_id = Column(
        String(20),
        ForeignKey(
            "transactions.transaction_id"
        ),
        unique=True
    )

    fraud_probability = Column(
        Numeric(5, 4)
    )

    prediction = Column(
        String(20)
    )

    risk_level = Column(
        String(20)
    )

    predicted_at = Column(
        DateTime,
        server_default=func.now()
    )