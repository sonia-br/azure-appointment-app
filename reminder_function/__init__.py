import datetime
import logging
from send_email import send_confirmation_email

def main(mytimer: dict) -> None:
    logging.info('Python timer function ran at %s', datetime.datetime.now())

    # Example: send a reminder
    send_confirmation_email("user@example.com", "Reminder: Your booking is tomorrow.")

