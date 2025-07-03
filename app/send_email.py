import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Cache clients for performance
_credential = DefaultAzureCredential()
_key_vault_url = os.environ.get("KEY_VAULT_URL")  # e.g. "https://your-vault.vault.azure.net"
_secret_client = SecretClient(vault_url=_key_vault_url, credential=_credential)

def send_confirmation_email(to_email, booking_info):
    if not to_email or not booking_info:
        raise ValueError("Missing 'to_email' or 'booking_info'")

    try:
        # Get the SendGrid API key from Key Vault
        sendgrid_api_key = _secret_client.get_secret("SENDGRID_API_KEY").value

        # Build the email
        message = Mail(
            from_email=Email("your_verified_sender@example.com", name="Booking System"),
            to_emails=to_email,
            subject="Your Booking Confirmation",
            html_content=f"<strong>Your booking is confirmed:</strong><br>{booking_info}"
        )
        message.add_content(Content("text/plain", f"Your booking is confirmed:\n{booking_info}"))

        # Send the email
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)

        logging.info(f"Email sent to {to_email}. Status: {response.status_code}")
        return response.status_code

    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {str(e)}")
        raise
