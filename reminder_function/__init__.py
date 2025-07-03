import datetime
import logging
from app.send_email import send_confirmation_email

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Timer trigger function ran at %s', utc_timestamp)

    try:
        # In production, replace this with a DB query for upcoming appointments
        to_email = "user@example.com"
        message = "Reminder: Your booking is tomorrow."

        send_confirmation_email(to_email, message)

    except Exception as e:
        logging.error(f"Error sending reminder email: {e}")
