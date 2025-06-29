import sqlite3
from app.validators import validate_user_input, validate_email

def connect_db(db_path='booking.db'): #function to open database file booking.db to run sql commands
    
    return sqlite3.connect(db_path) #returns an object of class Connection


def get_available_slots():
    connection = connect_db() #create an object of class Connection, calls function to connect to db
    cursor = connection.cursor() #create an object of class Cursor to run sql queries

    cursor.execute ("""SELECT * FROM slots WHERE id NOT IN ( SELECT slot_id FROM appointments)""")
    #select all rows from slots table without those that are already booked (NOT IN) by slot_id

    free_slots = cursor.fetchall() #gets all matching slots
    
    connection.close()
    return free_slots  #closes connection and returns slots


def check_available_slots(slot_id):
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute(
        """ SELECT COUNT(*) FROM appointments 
        WHERE slot_id = ? """, (slot_id,) # ? - placeholder to prevent sql injection
    ) #counts how many times slot_id appears in appointment table

    result = cursor.fetchone()[0] #gets first element of row  (id)
    #if result is 0, slot is not booked 

    connection.close()
    return result == 0 #returns true if result is equal to zero, if not zero then retuns false


def save_booking(name, email, mobile_number, slot_id):

    name, email, mobile_number = validate_user_input(name, email, mobile_number)

    if not check_available_slots(slot_id):
        raise ValueError("This slot is already booked")
    
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
    else:
        cursor.execute("INSERT INTO users (name, email, mobile_number) VALUES (?,?,?)", (name, email, mobile_number))
        user_id = cursor.lastrowid

    try:
        cursor.execute("""
            INSERT INTO appointments (user_id, slot_id)
            VALUES (?, ?)
        """, (user_id, slot_id))
        connection.commit()
    except sqlite3.IntegrityError:
        raise ValueError("This slot has just been booked. Please choose another.")
    finally:
        connection.close()


def handle_booking(name, email, mobile_number, slot_id):
    try:
        save_booking(name, email, mobile_number, slot_id)
        return ("Your appointment is booked!")
    except ValueError as e: #e stores error object that contain error message from save_booking
        return str(e)
    
def get_user_appointments(email):

    if not validate_email(email):
        raise ValueError("Invalid email.")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            appointments.id,
            slots.time,
            users.name,
            users.email,
            users.mobile_number
        FROM appointments
        JOIN users ON appointments.user_id = users.id
        JOIN slots ON appointments.slot_id = slots.id
        WHERE LOWER(users.email) = ?
        ORDER BY slots.time
    """, (email.lower(),))

    rows = cursor.fetchall()
    appointments = []
    for row in rows:
        appointment = {
            'id': row[0],
            'time': row[1],
            'name': row[2],
            'email': row[3],
            'phone': row[4],
            'notes': None
        }
        appointments.append(appointment)
    connection.close()
    return appointments




