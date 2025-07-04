from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mssql import BIT

db = SQLAlchemy()

class Slot(db.Model):
    __tablename__ = 'slots'  # explicitly match the table name
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Integer, default=1, nullable=False)

    appointments = db.relationship('Appointment', back_populates='slot')

class Appointment(db.Model):
    __tablename__ = 'appointments'  # explicitly match the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)

    slot = db.relationship('Slot', back_populates='appointments')
