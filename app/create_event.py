import requests
import json
import os
from msal import ConfidentialClientApplication

def get_access_token():
    app = ConfidentialClientApplication(
        client_id=os.environ['MS_CLIENT_ID'],
        client_credential=os.environ['MS_CLIENT_SECRET'],
        authority=f"https://login.microsoftonline.com/{os.environ['MS_TENANT_ID']}"
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return result['access_token']

def create_calendar_event(token, user_email, subject, start_time, end_time):
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/calendar/events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    event = {
        "subject": subject,
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(event))
    print("Event created:", response.status_code)

