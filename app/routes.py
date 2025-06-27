from flask import render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from app.booking_service import get_available_slots, handle_booking

def init_routes(app):
    @app.route('/')
    def index():
        """Home page route"""
        return render_template('index.html')

    @app.route('/slots')
    def view_slots():
        """View available appointment slots"""
        # TODO: Integrate with database to get actual slots
        # This is a placeholder for demonstration
        # slots = [
        #     {'time': '09:00', 'available': True},
        #     {'time': '10:00', 'available': True},
        #     {'time': '11:00', 'available': False},
        #     {'time': '14:00', 'available': True},
        # ]
        db_slots = get_available_slots()
        slots = [{'id': row[0], 'time': row[1], 'available': True} for row in db_slots]
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
            
            # # TODO: Add validation and database integration
            # if not all([slot_time, name, email]):
            #     flash('Please fill in all fields', 'error')
            #     return redirect(url_for('book_appointment'))
                
            # # TODO: Save booking to database
            # flash('Appointment booked successfully!', 'success')
            # return redirect(url_for('index'))
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

    @app.route('/my-appointments')
    def my_appointments():
        """View user's appointments"""
        # TODO: Integrate with database to get user's appointments
        return render_template('my_appointments.html')
