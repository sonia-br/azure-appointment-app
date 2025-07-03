import os
import requests
import logging
from msal import ConfidentialClientApplication

def get_access_token():
    try:
        app = ConfidentialClientApplication(
            client_id=os.environ['MS_CLIENT_ID'],
            client_credential=os.environ['MS_CLIENT_SECRET'],
            authority=f"https://login.microsoftonline.com/{os.environ['MS_TENANT_ID']}"
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" in result:
            return result["access_token"]
        else:
            logging.error(f"MSAL auth failed: {result.get('error_description', result)}")
            raise RuntimeError("Failed to obtain access token.")
    except Exception as e:
        logging.error(f"Error getting access token: {str(e)}")
        raise

def create_calendar_event(token, user_email, subject, start_time, end_time):
    if not all([token, user_email, subject, start_time, end_time]):
        raise ValueError("Missing required calendar event fields")

    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/calendar/events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    event = {
        "subject": subject,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"}
    }

    try:
        response = requests.post(url, headers=headers, json=event)
        if response.status_code in (200, 201):
            logging.info(f"Calendar event created for {user_email}")
        else:
            logging.error(f"Failed to create event: {response.status_code} - {response.text}")
            raise RuntimeError(f"Graph API error: {response.status_code}")
    except Exception as e:
        logging.error(f"Error creating calendar event: {str(e)}")
        raise
