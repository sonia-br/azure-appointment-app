from dotenv import load_dotenv
load_dotenv()

from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object('config.Config')
    
    return app
