from dotenv import load_dotenv
load_dotenv()

import os
import logging
import requests
from msal import ConfidentialClientApplication

def get_access_token():
    try:
        app = ConfidentialClientApplication(
            client_id=os.getenv("MS_CLIENT_ID"),
            client_credential=os.getenv("MS_CLIENT_SECRET"),
            authority=f"https://login.microsoftonline.com/{os.getenv('MS_TENANT_ID')}"
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" in result:
            return result["access_token"]
        else:
            logging.error(f"MSAL auth failed: {result}")
            raise RuntimeError("Could not get access token.")
    except Exception as e:
        logging.error(f"Access token error: {e}")
        raise

def create_calendar_event(token, user_email, subject, start_time, end_time):
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/calendar/events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    event = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": "This is your confirmed booking."
        },
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC"
        },
        "location": {
            "displayName": "Online"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=event)
        if response.status_code in (200, 201):
            logging.info(f"Calendar event created for {user_email}")
        else:
            logging.error(f"Calendar creation failed: {response.status_code} - {response.text}")
            raise RuntimeError("Calendar event creation failed.")
    except Exception as e:
        logging.error(f"Graph API error: {e}")
        raise
