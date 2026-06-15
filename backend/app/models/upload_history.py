from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.database.base import Base


class UploadHistory(Base):

    __tablename__ = "upload_history"

    upload_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    file_name = Column(
        String(255)
    )

    records_count = Column(
        Integer
    )

    fraud_detected = Column(
        Integer
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )