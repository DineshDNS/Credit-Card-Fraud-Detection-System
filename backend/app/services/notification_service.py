import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)

print("=" * 50)
print("EMAIL =", EMAIL_ADDRESS)
print("PASSWORD =", EMAIL_PASSWORD)
print("=" * 50)

def send_email_alert(
    customer,
    transaction,
    prediction,
    risk_level
):

    subject = (
        "Fraud Alert - Suspicious Transaction Detected"
    )

    body = f"""
Dear {customer.customer_name},

A potentially fraudulent transaction has been detected.

Transaction Details
-------------------------
Transaction ID : {transaction.transaction_id}
Amount         : ₹{transaction.amount}
Merchant       : {transaction.merchant}
Location       : {transaction.location}

Prediction     : {prediction}
Risk Level     : {risk_level}

If this transaction was authorized by you,
no further action is required.

If this transaction was NOT made by you,
please contact customer support immediately.

Regards,
Credit Card Fraud Detection Team
"""

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = EMAIL_ADDRESS
    message["To"] = customer.email

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(
                message
            )

        print(
            f"Email sent to "
            f"{customer.email}"
        )

    except Exception as e:

        print(
            f"Email failed: {e}"
        )


def send_sms_alert(
    customer,
    transaction,
    prediction
):

    print("\n" + "=" * 50)

    print("SMS ALERT SENT")

    print(
        f"Phone: {customer.phone}"
    )

    print(
        f"Transaction ID: "
        f"{transaction.transaction_id}"
    )

    print(
        f"Amount: ₹{transaction.amount}"
    )

    print(
        f"Prediction: {prediction}"
    )

    print("=" * 50)