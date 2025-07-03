from flask import render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from app.booking_service import get_available_slots, handle_booking, get_user_appointments, connect_db
from app.send_email import send_confirmation_email
from app.create_event import get_access_token, create_calendar_event

def init_routes(app):
    
    @app.route('/')
    def index():
        """Home page route"""
        return render_template('index.html')

    @app.route('/slots')
    def view_slots():
        db_slots = get_available_slots()
        slots = [{'id': row[0], 'time': row[1], 'available': True} for row in db_slots]
        return render_template('slots.html', slots=slots)

    @app.route('/book', methods=['GET', 'POST'])
    def book_appointment():
        """Book an appointment"""
        if request.method == 'POST':
            slot_id = request.form.get('slot_id', '').strip()
            slot_time = request.form.get('slot_time', '').strip()
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            mobile = request.form.get('phone', '').strip()

            # ✅ Validate slot ID before converting
            if not slot_id.isdigit():
                flash("Invalid or missing slot ID.", "error")
                return redirect(url_for('book_appointment'))

            if not all([slot_time, name, email]):
                flash("Please fill in all required fields.", "error")
                return redirect(url_for('book_appointment'))

            try:
                # Save the booking (custom DB logic)
                message = handle_booking(name, email, mobile, int(slot_id))
                flash(message, 'success')

                # Send confirmation email
                booking_info = f"Your appointment is confirmed for {slot_time}."
                send_confirmation_email(email, booking_info)

                # Create calendar event (30 mins duration)
                token = get_access_token()
                subject = f"Booking with {name}"
                start_time = slot_time  # must be ISO 8601 format
                end_time = (datetime.fromisoformat(start_time) + timedelta(minutes=30)).isoformat()
                create_calendar_event(token, email, subject, start_time, end_time)

                return redirect(url_for('book_appointment',
                                        slot_id=slot_id,
                                        slot_time=slot_time))

            except Exception as e:
                flash(f"Error: {str(e)}", "error")
                return redirect(url_for('book_appointment'))

        # GET request — show booking form
        return render_template('book.html',
                               slot_time=request.args.get('slot_time', ''),
                               slot_id=request.args.get('slot_id', ''))
    @app.route('/my-appointments', methods=['GET'])
    def my_appointments():
        """View user's appointments"""
        email = request.args.get('email', '').strip()  # ✅ Define it here
        appointments = None

        if email:
            try:
                appointments = get_user_appointments(email)
            except ValueError as e:
                flash(str(e), 'error')

        return render_template('my_appointments.html', appointments=appointments)


    
    @app.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
    def cancel_appointment(appointment_id):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        connection.commit()
        connection.close()

        flash("Appointment canceled.", "success")
        return redirect(url_for('my_appointments'))

