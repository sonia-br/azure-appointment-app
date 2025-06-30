import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_confirmation_email(to_email, booking_info):
    message = Mail(
        from_email='your_verified_sender@example.com',
        to_emails=to_email,
        subject='Booking Confirmation',
        html_content=f'<strong>Your booking is confirmed:</strong><br>{booking_info}'
    )
    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print("Email sent:", response.status_code)
    except Exception as e:
        print("SendGrid Error:", e)

