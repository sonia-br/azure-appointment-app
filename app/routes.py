from flask import render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from .models import db, Slot, Appointment
from app.booking_service import get_available_slots, handle_booking, get_user_appointments, connect_db

def init_routes(app):
    @app.route('/')
    def index():
        """Home page route"""
        return render_template('index.html')

    @app.route('/slots')
    def view_slots():
        """View available appointment slots"""
        slots = get_available_slots()
        return render_template('slots.html', slots=slots)

    @app.route('/book', methods=['GET', 'POST'])
    def book_appointment():
        """Book an appointment"""
        if request.method == 'POST':
            slot_id = request.form.get('slot_id')
            slot_time = request.form.get('slot_time')
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('phone')
            

            try:
                message = handle_booking(name, email, mobile, int(slot_id))
                flash(message, 'success')
                return redirect(url_for('book_appointment', 
                                        slot_id=slot_id,
                                        slot_time=request.form.get('slot_time', '')))
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('book_appointment'))
            
        return render_template('book.html',
                           slot_time=request.args.get('slot_time', ''),
                           slot_id=request.args.get('slot_id', ''))

    @app.route('/my-appointments', methods=['GET'])
    def my_appointments():
        """View user's appointments"""
        email = request.args.get('email', '').strip()
        appointments = None
        if email:
            try:
                appointments = get_user_appointments(email)
            except ValueError as e:
                flash(str(e), 'error')

        return render_template('my_appointments.html', appointments=appointments)
    
    @app.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
    def cancel_appointment(appointment_id):
        """Cancel appointment"""
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            slot = Slot.query.get(appointment.slot_id)
            slot.available = True
            db.session.delete(appointment)
            db.session.commit()
            flash("Appointment canceled.", "success")
        else:
            flash("Appointment not found.", "error")

        return redirect(url_for('my_appointments'))