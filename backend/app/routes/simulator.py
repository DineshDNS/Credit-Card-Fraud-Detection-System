from fastapi import APIRouter
from fastapi import Depends

from app.database.connection import (
    SessionLocal
)

from app.core.dependencies import (
    get_current_admin
)

from app.services import simulator_service

import threading

from sqlalchemy.orm import Session

from app.database.connection import (
    get_db,
    SessionLocal
)

from app.models.transaction import Transaction

router = APIRouter()


@router.post("/simulator/start")
def start_simulator(

    current_admin: str = Depends(
        get_current_admin
    )

):

    if (
        simulator_service.SIMULATOR_THREAD
        and
        simulator_service.SIMULATOR_THREAD.is_alive()
    ):

        return {
            "message":
            "Simulator already running"
        }

    simulator_service.SIMULATOR_RUNNING = True

    simulator_service.SIMULATOR_THREAD = (
        threading.Thread(
            target=
            simulator_service.simulator_worker,
            args=(SessionLocal,),
            daemon=True
        )
    )

    simulator_service.SIMULATOR_THREAD.start()

    return {
        "message":
        "Simulator Started"
    }


@router.post("/simulator/stop")
def stop_simulator(

    current_admin: str = Depends(
        get_current_admin
    )

):

    simulator_service.SIMULATOR_RUNNING = False

    simulator_service.SIMULATOR_THREAD = None

    return {
        "message":
        "Simulator Stopped"
    }


@router.get("/simulator/status")
def simulator_status():

    running = False

    if (
        simulator_service.SIMULATOR_THREAD
        and
        simulator_service.SIMULATOR_THREAD.is_alive()
    ):
        running = True

    return {
        "running": running
    }

@router.get("/simulator/recent-transactions")
def recent_transactions(
    db: Session = Depends(get_db),
    current_admin: str = Depends(
        get_current_admin
    )
):

    transactions = (

        db.query(Transaction)

        .filter(
            Transaction.transaction_id.like(
                "SIMTXN%"
            )
        )

        .order_by(
            Transaction.transaction_time.desc()
        )

        .limit(20)

        .all()

    )

    return transactions