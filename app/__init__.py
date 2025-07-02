from flask import Flask
import os
from .models import db

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    
    
    return app
