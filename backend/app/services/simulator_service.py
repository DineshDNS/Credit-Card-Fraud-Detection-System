import random
import time

from datetime import datetime

from app.models.customer import Customer
from app.models.transaction import Transaction

from app.services.production_prediction_service import (
    predict_transaction
)

SIMULATOR_RUNNING = False

SIMULATOR_THREAD = None

TRANSACTION_COUNTER = 0

LAST_FRAUD_AT = 0


DEMO_CUSTOMERS = [

    ("C001", "Dinesh", "Chennai"),
    ("C002", "Kumar", "Bangalore"),
    ("C003", "Ravi", "Hyderabad"),
    ("C004", "Priya", "Mumbai"),
    ("C005", "Arun", "Coimbatore"),

    ("C006", "Deepa", "Chennai"),
    ("C007", "Karthik", "Bangalore"),
    ("C008", "Nisha", "Hyderabad"),
    ("C009", "Vijay", "Mumbai"),
    ("C010", "Anitha", "Coimbatore"),

    ("C011", "Suresh", "Chennai"),
    ("C012", "Meena", "Madurai"),
    ("C013", "Rahul", "Pune"),
    ("C014", "Divya", "Delhi"),
    ("C015", "Harish", "Kochi"),

    ("C016", "Keerthana", "Trichy"),
    ("C017", "Manoj", "Salem"),
    ("C018", "Pooja", "Bangalore"),
    ("C019", "Ajith", "Chennai"),
    ("C020", "Lavanya", "Hyderabad"),

    ("C021", "Gokul", "Mumbai"),
    ("C022", "Sneha", "Pune"),
    ("C023", "Vignesh", "Coimbatore"),
    ("C024", "Aarthi", "Madurai"),
    ("C025", "Ramesh", "Delhi"),

    ("C026", "Kavya", "Kochi"),
    ("C027", "Sathish", "Trichy"),
    ("C028", "Monika", "Salem"),
    ("C029", "Prakash", "Bangalore"),
    ("C030", "Revathi", "Chennai"),

    ("C031", "Bharath", "Hyderabad"),
    ("C032", "Shalini", "Mumbai"),
    ("C033", "Naveen", "Pune"),
    ("C034", "Janani", "Coimbatore"),
    ("C035", "Mohan", "Madurai"),

    ("C036", "Gayathri", "Delhi"),
    ("C037", "Kishore", "Kochi"),
    ("C038", "Sindhu", "Trichy"),
    ("C039", "Arvind", "Salem"),
    ("C040", "Vaishnavi", "Bangalore"),

    ("C041", "Dharun", "Chennai"),
    ("C042", "Preethi", "Hyderabad"),
    ("C043", "Lokesh", "Mumbai"),
    ("C044", "Akshaya", "Pune"),
    ("C045", "Saravanan", "Coimbatore"),

    ("C046", "Nandhini", "Madurai"),
    ("C047", "Yuvaraj", "Delhi"),
    ("C048", "Ritika", "Kochi"),
    ("C049", "Balaji", "Trichy"),
    ("C050", "Aishwarya", "Salem")

]


def simulator_worker(db_factory):

    global SIMULATOR_RUNNING
    global TRANSACTION_COUNTER
    global LAST_FRAUD_AT

    while SIMULATOR_RUNNING:

        db = db_factory()

        try:

            (
                customer_id,
                customer_name,
                home_location
            ) = random.choice(
                DEMO_CUSTOMERS
            )

            customer = (

                db.query(Customer)

                .filter(
                    Customer.customer_id
                    == customer_id
                )

                .first()

            )

            if not customer:

                customer = Customer(

                    customer_id=
                        customer_id,

                    customer_name=
                        customer_name,

                    email=
                        "dineshkarthickklm92@gmail.com",

                    phone=
                        "9876543210",

                    home_location=
                        home_location
                )

                db.add(customer)

                db.commit()

            TRANSACTION_COUNTER += 1

            is_fraud = False

            # -----------------------------
            # Fraud Logic
            # -----------------------------

            if (
                TRANSACTION_COUNTER
                - LAST_FRAUD_AT
            ) >= 20:

                if random.random() < 0.03:

                    is_fraud = True

                    LAST_FRAUD_AT = (
                        TRANSACTION_COUNTER
                    )

            # -----------------------------
            # Fraud Transaction
            # -----------------------------

            if is_fraud:

                amount = random.randint(
                    300000,
                    3000000
                )

                location = random.choice([

                    "Dubai",
                    "Singapore",
                    "London",
                    "New York",
                    "Tokyo"

                ])

                merchant = random.choice([

                    "Crypto Exchange",
                    "Foreign Luxury Store",
                    "International Electronics",
                    "Offshore Payment Gateway"

                ])

            # -----------------------------
            # Genuine Transaction
            # -----------------------------

            else:

                amount = random.randint(
                    100,
                    10000
                )

                location = home_location

                merchant = random.choice([

                    "Amazon",
                    "Flipkart",
                    "Swiggy",
                    "Zomato",
                    "Myntra"

                ])

            txn_id = (
                f"SIMTXN"
                f"{random.randint(100000,999999)}"
            )

            transaction = Transaction(

                transaction_id=
                    txn_id,

                user_id=
                    customer_id,

                merchant=
                    merchant,

                location=
                    location,

                transaction_type=
                    "Online",

                amount=
                    amount,

                transaction_time=
                    datetime.utcnow(),

                actual_class=0

            )

            db.add(transaction)

            db.commit()

            db.refresh(transaction)

            predict_transaction(
                db,
                transaction
            )

        except Exception as e:

            print(
                "Simulator Error:",
                str(e)
            )

        finally:

            db.close()

        time.sleep(5)