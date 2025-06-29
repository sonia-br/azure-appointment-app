import pytest

from app import booking_service


# print("--- Available Slots Before Booking ---")
# slots = get_available_slots()
# print(slots) 

# print("\n--- Try Booking Slot 1 ---")
# result1 = book_appointment("Alex", "alex@example.com", "017612345678", 1)
# print(result1)  

# print("\n--- Try Booking Slot 1 Again ---")
# result2 = book_appointment("Bob", "bob@example.com", "017698765432", 1)
# print(result2)  #should print "This slot is already booked"

# print("\n--- Available Slots After Booking ---")
# slots_after = get_available_slots()
# print(slots_after)  #should show only 2 remaining slots


def test_booking_with_invalid_email():
    result = booking_service.handle_booking("Alex", "alex.com", "017612345678", 1)
    assert result == "Invalid email."

def test_booking_with_empty_name():
    result = booking_service.handle_booking(" ", "alex@example.com", "017612345678", 1)
    assert result == "Fields can't be empty"

def test_booking_with_invalid_mobile():
    result = booking_service.handle_booking("Alex", "alex@example.com", "abc123", 1)
    assert result == "Invalid mobile number. Number must contain only digits and 11 characters"

def test_booking_with_invalid_name():
    result = booking_service.handle_booking("!!", "alex@example.com", "017612345678", 1)
    assert result == "Invalid name. Name must contain at least 2 letters."

def test_successful_booking(setup_test_db):
    result = booking_service.handle_booking("Alice", "alice@example.com", "01761234567", 3)
    assert result == "Your appointment is booked!"

def test_double_booking_same_slot(setup_test_db):
    booking_service.handle_booking("User One", "one@example.com", "01761234567", 1)
    result = booking_service.handle_booking("User Two", "two@example.com", "01761230000", 1)
    assert result == "This slot is already booked"

def test_booking_creates_user_if_new(setup_test_db):
    booking_service.handle_booking("New User", "newuser@example.com", "01761111111", 2)
    connection = booking_service.connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", ("newuser@example.com",))
    user = cursor.fetchone()
    connection.close()
    assert user is not None

def test_slot_removed_after_booking(setup_test_db):
    before = booking_service.get_available_slots()
    booking_service.handle_booking("User", "user@example.com", "01761234567", 2)
    after = booking_service.get_available_slots()
    assert len(after) == len(before) - 1

def test_get_user_appointments_returns_data(setup_test_db):
    booking_service.handle_booking("User", "check@example.com", "01761234567", 3)
    appointments = booking_service.get_user_appointments("check@example.com")
    assert len(appointments) == 1
    assert appointments[0]['time'] == '2025-07-12 16:00:00'

def test_cancel_appointment_removes_it(setup_test_db):
    booking_service.handle_booking("Cancel Me", "cancel@example.com", "01760000000", 2)
    connection = booking_service.connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM appointments WHERE slot_id = 2")
    appointment_id = cursor.fetchone()[0]

    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    connection.commit()

    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    assert cursor.fetchone() is None
    connection.close()