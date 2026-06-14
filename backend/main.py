from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.transactions import (router as transaction_router)
from app.routes.dashboard import (
    router as dashboard_router
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Credit Card Fraud Detection API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

app.include_router(
    auth_router
)

app.include_router(
    transaction_router
)


app.include_router(
    dashboard_router
)

from app.routes.predictions import (
    router as prediction_router
)

app.include_router(
    prediction_router
)

from app.routes.alerts import (
    router as alerts_router
)

app.include_router(
    alerts_router
)

from app.routes.fraud_predictions import(router as fraud_predictions)

app.include_router(
    fraud_predictions
)

@app.get("/")
def home():

    return {
        "message":
        "Fraud Detection API Running"
    }