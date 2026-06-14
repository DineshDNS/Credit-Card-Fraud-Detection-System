from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Integer

from app.database.base import Base


class MLTransaction(Base):

    __tablename__ = "ml_transactions"

    transaction_id = Column(
        String(20),
        primary_key=True
    )

    Time = Column(Float)

    V1 = Column(Float)
    V2 = Column(Float)
    V3 = Column(Float)
    V4 = Column(Float)
    V5 = Column(Float)
    V6 = Column(Float)
    V7 = Column(Float)
    V8 = Column(Float)
    V9 = Column(Float)
    V10 = Column(Float)
    V11 = Column(Float)
    V12 = Column(Float)
    V13 = Column(Float)
    V14 = Column(Float)
    V15 = Column(Float)
    V16 = Column(Float)
    V17 = Column(Float)
    V18 = Column(Float)
    V19 = Column(Float)
    V20 = Column(Float)
    V21 = Column(Float)
    V22 = Column(Float)
    V23 = Column(Float)
    V24 = Column(Float)
    V25 = Column(Float)
    V26 = Column(Float)
    V27 = Column(Float)
    V28 = Column(Float)

    Amount = Column(Float)

    Merchant = Column(
        String(100)
    )

    Location = Column(
        String(100)
    )

    TransactionType = Column(
        String(20)
    )

    TransactionFrequency = Column(Integer)

    UserAvgAmount = Column(Float)

    TimeGap = Column(Float)

    LocationDeviation = Column(Integer)

    UnusualSpending = Column(Integer)

    Hour = Column(Integer)

    NightTransaction = Column(Integer)

    HighAmountFlag = Column(Integer)

    RapidTransaction = Column(Integer)