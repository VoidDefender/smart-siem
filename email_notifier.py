import os
import smtplib
import logging
from email.message import EmailMessage
from dotenv import load_dotenv

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_RECEIVER = os.getenv("ALERT_RECEIVER")

# ---------------------------------------------------
# Logging configuration
# ---------------------------------------------------
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------------
# Send Email Function
# ---------------------------------------------------
def send_email_alert(subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = ALERT_RECEIVER
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        logging.info("Email alert sent successfully.")

    except Exception as e:
        logging.error(f"Email sending failed: {e}")
