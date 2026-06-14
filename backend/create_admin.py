from app.database.connection import SessionLocal
from app.models.admin import Admin
from app.core.security import hash_password

db = SessionLocal()

admin = Admin(
    username="admin",
    email="admin@fraud.com",
    password_hash=hash_password(
        "admin123"
    )
)

db.add(admin)

db.commit()

db.close()

print(
    "Admin Created Successfully"
)