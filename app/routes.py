from flask import render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from .models import db, Slot, Appointment

def init_routes(app):
    # TODO: Add user authentication (Flask-Login)
    # TODO: Add admin interface for managing slots and appointments
    # TODO: Add slot cancellation and rescheduling
    # TODO: Add email notifications for bookings/cancellations
    # TODO: Add recurring slot generation
    # TODO: Add support for slot duration per slot
    # TODO: Add date field to Slot model for multi-day support
    # TODO: Add pagination for slots and appointments lists

    @app.route('/')
    def index():
        """Home page route"""
        return render_template('index.html')

    @app.route('/slots')
    def view_slots():
        """View available appointment slots, filterable by date and time"""
        # TODO: Update Slot model to include a date field (date = db.Column(db.Date, nullable=False))
        date_str = request.args.get('date')
        time_str = request.args.get('time')
        query = Slot.query
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter_by(date=date_obj)
            except ValueError:
                flash('Invalid date format. Use YYYY-MM-DD.', 'error')
        if time_str:
            query = query.filter_by(time=time_str)
        slots = query.all()
        return render_template('slots.html', slots=slots)

    @app.route('/book', methods=['GET', 'POST'])
    def book_appointment():
        """Book an appointment"""
        if request.method == 'POST':
            slot_id = request.form.get('slot_id')
            name = request.form.get('name')
            email = request.form.get('email')

            # Validation
            if not all([slot_id, name, email]):
                flash('Please fill in all fields', 'error')
                return redirect(url_for('book_appointment'))

            slot = Slot.query.filter_by(id=slot_id, available=True).first()
            if not slot:
                flash('Selected slot is not available.', 'error')
                return redirect(url_for('book_appointment'))

            # Save booking to database
            appointment = Appointment(name=name, email=email, slot_id=slot.id)
            slot.available = False
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('index'))

        # TODO: Allow filtering available slots by date for booking
        slots = Slot.query.filter_by(available=True).all()
        return render_template('book.html', slots=slots)

    @app.route('/my-appointments')
    def my_appointments():
        """View user's appointments"""
        # For demo: get appointments by email from query param
        # TODO: Link appointments to authenticated user when auth is added
        email = request.args.get('email')
        appointments = []
        if email:
            appointments = Appointment.query.filter_by(email=email).all()
        return render_template('my_appointments.html', appointments=appointments)
