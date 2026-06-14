from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):

    transaction_id: str
    user_id: str

    merchant: str
    location: str

    transaction_type: str

    amount: float

    transaction_time: datetime

    actual_class: int