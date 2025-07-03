
from app import create_app
from app.routes import init_routes

app = create_app()
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

﻿import logging
from datetime import datetime

from send_email import send_confirmation_email
from create_event import get_access_token, create_calendar_event

def main():
   
    user_email = "sofyaborlykovagmail.onmicrosoft.com"

    # 📅 Booking time (adjust as needed)
    start_dt = datetime(2025, 5, 20, 14, 0)
    end_dt = datetime(2025, 5, 20, 15, 0)

    # 📝 Auto-generate message and event times
    booking_info = f"Booking: {start_dt.strftime('%B %d, %Y at %I:%M %p')}"
    start = start_dt.isoformat()
    end = end_dt.isoformat()
    subject = "Booking with You"

    try:
        logging.info("Sending confirmation email...")
        send_confirmation_email(user_email, booking_info)
        logging.info("✅ Email sent successfully.")

        logging.info("Getting Microsoft Graph access token...")
        token = get_access_token()

        logging.info("Creating calendar event...")
        create_calendar_event(token, user_email, subject, start, end)
        logging.info("✅ Calendar event created.")

    except Exception as e:
        logging.error(f"❌ Error during booking processing: {str(e)}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

