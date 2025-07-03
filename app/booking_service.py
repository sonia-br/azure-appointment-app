from app.models import db, Slot, Appointment
from app.validators import validate_user_input, validate_email
from sqlalchemy.exc import IntegrityError


def get_available_slots():
    slots = Slot.query.filter_by(Slot.available == 1).all()
    print("Available slots:", slots)  # Debug
    return slots

def check_available_slots(slot_id):
    slot = Slot.query.filter_by(Slot.id == slot_id, Slot.available == 1).first()
    return slot is not None

def save_booking(name, email, mobile_number, slot_id):
    name, email, mobile_number = validate_user_input(name, email, mobile_number)

    if not check_available_slots(slot_id):
        raise ValueError("This slot is already booked")

    slot = Slot.query.get(slot_id)
    if not slot:
        raise ValueError("Slot not found")
    
    appointment = Appointment(
        name=name,
        email=email,
        slot_id=slot_id
    )
    slot.available = False

    try:
        db.session.add(appointment)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("The slot has been booked by someone else. Please choose another slot.")


def handle_booking(name, email, mobile_number, slot_id):
    try:
        save_booking(name, email, mobile_number, slot_id)
        return ("Your appointment is booked!")
    except ValueError as e: #e stores error object that contain error message from save_booking
        return str(e)

def get_user_appointments(email):
    if not validate_email(email):
        raise ValueError("Invalid email.")

    return Appointment.query.filter_by(email=email.lower()).join(Slot).order_by(Slot.time).all()




