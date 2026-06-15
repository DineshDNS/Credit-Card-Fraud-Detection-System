from app.database.connection import engine
from app.database.base import Base

from app.models.admin import Admin
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.models.fraud_prediction import FraudPrediction
from app.models.alert import Alert
from app.models.audit_log import AuditLog
from app.models.ml_transaction import MLTransaction

from app.models.upload_history import UploadHistory

Base.metadata.create_all(
    bind=engine
)

print(
    "All tables created successfully"
)