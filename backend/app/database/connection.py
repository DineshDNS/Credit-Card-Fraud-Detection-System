from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# -----------------------------
# SQLAlchemy Engine
# -----------------------------

engine = create_engine(
    DATABASE_URL
)

# -----------------------------
# Session Factory
# -----------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------
# Dependency
# -----------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()