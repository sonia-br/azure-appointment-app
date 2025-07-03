import logging
from send_email import send_confirmation_email
from create_event import get_access_token, create_calendar_event

def main():
    user_email = "user@example.com"
    booking_info = "Booking: May 20, 2025 at 2 PM"
    subject = "Booking with You"
    start = "2025-05-20T14:00:00"
    end = "2025-05-20T15:00:00"

    try:
        logging.info("Sending confirmation email...")
        send_confirmation_email(user_email, booking_info)
        logging.info("Email sent successfully.")

        logging.info("Getting Microsoft Graph access token...")
        token = get_access_token()

        logging.info("Creating calendar event...")
        create_calendar_event(token, user_email, subject, start, end)
        logging.info("Calendar event created.")

    except Exception as e:
        logging.error(f"Error during booking processing: {str(e)}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
