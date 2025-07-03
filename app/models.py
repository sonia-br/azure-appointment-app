from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mssql import BIT

db = SQLAlchemy()

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Integer, default=1, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    slot = db.relationship('Slot', backref=db.backref('appointments', lazy=True))
