import sqlite3

def connect_db(): #function to open database file booking.db to run sql commands
    
    return sqlite3.connect('booking.db') #returns an object of class Connection

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
    if not check_available_slots(slot_id):
        raise ValueError("This slot is already booked")
    
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO appointments (name, email, mobile_number, slot_id)
        VALUES (?, ?, ?, ?)
    """, (name, email, mobile_number, slot_id))
    
    connection.commit()
    connection.close()

def book_appointment(name, email, mobile_number, slot_id):
    try:
        save_booking(name, email, mobile_number, slot_id)
        return ("Your appointment is booked!")
    except ValueError as e: #e stores error object that contain error message from save_booking
        return str(e)
    




