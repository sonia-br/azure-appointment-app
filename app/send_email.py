from dotenv import load_dotenv
load_dotenv()  # Load .env variables

import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Configure logging
logger = logging.getLogger("azure.email")
logging.basicConfig(level=logging.INFO)

def get_sendgrid_api_key():
    """Retrieve the SendGrid API key from .env or Azure Key Vault."""
    api_key = os.environ.get("SENDGRID_API_KEY")
    if api_key:
        logger.info("✅ SendGrid API key loaded from environment.")
        return api_key

    key_vault_url = os.environ.get("KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("SENDGRID_API_KEY not found and KEY_VAULT_URL is not set.")

    logger.info("🔐 Fetching SendGrid API key from Azure Key Vault...")
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

    return secret_client.get_secret("sendgrid-api-key").value

def send_confirmation_email(to_email, booking_info):
    """Send a booking confirmation email via SendGrid."""
    if not to_email or not booking_info:
        raise ValueError("Missing 'to_email' or 'booking_info'")

    try:
        api_key = get_sendgrid_api_key()

        message = Mail(
            from_email=Email("stevenwielis9@gmail.com", name="Booking System"),
            to_emails=to_email,
            subject="Your Booking Confirmation",
            html_content=f"<strong>Your booking is confirmed:</strong><br>{booking_info}"
        )
        message.add_content(Content("text/plain", f"Your booking is confirmed:\n{booking_info}"))

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        logger.info(f"📧 Email sent to {to_email}. Status: {response.status_code}")
        return response.status_code

    except Exception as e:
        logger.error(f"❌ Failed to send email to {to_email}: {str(e)}")
        raise
