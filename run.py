from app import create_app
from app.routes import init_routes
from app.models import db

app = create_app()
init_routes(app)

# Temporary: run table creation
with app.app_context():
    db.create_all()
