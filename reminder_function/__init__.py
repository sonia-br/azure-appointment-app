import datetime
import logging
import os

from sqlalchemy import create_engine, text
from app.send_email import send_confirmation_email

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_now = datetime.datetime.utcnow()
    logging.info(f"Reminder function ran at {utc_now.isoformat()}")

    try:
        # Load DB connection string (use secret from Azure App Settings)
        db_url = os.environ["DB_URL"]

        # Create SQLAlchemy engine
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Select bookings for tomorrow
            query = text("""
                SELECT email, booking_date 
                FROM bookings 
                WHERE CAST(booking_date AS DATE) = CAST(GETDATE() + 1 AS DATE)
            """)
            result = conn.execute(query)

            for row in result:
                to_email = row.email
                booking_time = row.booking_date.strftime('%Y-%m-%d %H:%M')
                message = f"Reminder: Your booking is scheduled for {booking_time}."
                send_confirmation_email(to_email, message)

    except Exception as e:
        logging.error(f"Error in reminder function: {e}")
