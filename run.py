from send_email import send_confirmation_email
from create_event import get_access_token, create_calendar_event

if __name__ == "__main__":
    user_email = "user@example.com"
    booking_info = "Booking: May 20, 2025 at 2 PM"
    start = "2025-05-20T14:00:00"
    end = "2025-05-20T15:00:00"

    send_confirmation_email(user_email, booking_info)
    token = get_access_token()
    create_calendar_event(token, user_email, "Booking with You", start, end)
