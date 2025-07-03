import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

KEY_VAULT_URL = "https://appointment-kv.vault.azure.net/"

# using managed identity
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

def get_secret(name, default=None):
    try:
        return client.get_secret(name).value
    except Exception:
        return default
    

class Config:
    """Base configuration."""
    SECRET_KEY = get_secret('SECRET-KEY')
    SQLALCHEMY_DATABASE_URI = get_secret('DATABASE-URL') #'sqlite:///booking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # print("DB URI:", SQLALCHEMY_DATABASE_URI) debug

    
    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = get_secret('sendgrid-api-key')
    
    # Appointment settings
    APPOINTMENT_DURATION = 30  # minutes
    WORKING_HOURS_START = 9  # 9 AM
    WORKING_HOURS_END = 17  # 5 PM
    BOOKING_DAYS_AHEAD = 14  # Allow booking up to 14 days ahead

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
