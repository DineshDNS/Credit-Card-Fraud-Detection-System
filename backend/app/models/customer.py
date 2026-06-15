from sqlalchemy import Column
from sqlalchemy import String

from app.database.base import Base


class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        String(20),
        primary_key=True
    )

    customer_name = Column(
        String(100)
    )

    email = Column(
        String(100)
    )

    phone = Column(
        String(20)
    )

    home_location = Column(
        String(100)
    )