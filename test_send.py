from app.send_email import send_confirmation_email

test_email = "stevenwgaming@gmail.com"
test_info = "Booking ID: 12345, Date: 2025-07-04, Time: 10:00 AM"

try:
    status = send_confirmation_email(test_email, test_info)
    print(f"Email send status: {status}")
except Exception as err:
    print(f"Error occurred: {err}")
