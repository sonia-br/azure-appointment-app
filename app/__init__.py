from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object('config.Config')
    
    # Register blueprints here if needed
    
    return app

import logging
import azure.functions as func
from send_email import send_confirmation_email
from create_event import get_access_token, create_calendar_event
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()

        user_email = data.get("email")
        start_time = data.get("start_time")  # e.g. 2025-07-05T15:00:00
        end_time = data.get("end_time")      # e.g. 2025-07-05T16:00:00
        name = data.get("name", "Customer")

        if not all([user_email, start_time, end_time]):
            return func.HttpResponse("Missing required fields", status_code=400)

        # Format booking info for email
        dt = datetime.fromisoformat(start_time)
        booking_info = f"Booking for {name}: {dt.strftime('%B %d, %Y at %I:%M %p')}"

        send_confirmation_email(user_email, booking_info)

        token = get_access_token()
        subject = f"Booking with {name}"
        create_calendar_event(token, user_email, subject, start_time, end_time)

        return func.HttpResponse("Success", status_code=200)

    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        return func.HttpResponse("Internal server error", status_code=500)
