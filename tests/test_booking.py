import pytest

from app.booking_service import book_appointment, get_available_slots

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
    result = book_appointment("Alex", "alex.com", "017612345678", 1)
    assert result == "Invalid email."

def test_booking_with_empty_name():
    result = book_appointment(" ", "alex@example.com", "017612345678", 1)
    assert result == "Fields can't be empty"

def test_booking_with_invalid_mobile():
    result = book_appointment("Alex", "alex@example.com", "abc123", 1)
    assert result == "Invalid mobile number. Number must contain only digits and 11 characters"

def test_booking_with_invalid_name():
    result = book_appointment("!!", "alex@example.com", "017612345678", 1)
    assert result == "Invalid name. Name must contain at least 2 letters."