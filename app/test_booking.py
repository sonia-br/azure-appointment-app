from booking_service import get_available_slots, book_appointment

print("--- Available Slots Before Booking ---")
slots = get_available_slots()
print(slots) 

print("\n--- Try Booking Slot 1 ---")
result1 = book_appointment("Alex", "alex@example.com", "017612345678", 1)
print(result1)  

print("\n--- Try Booking Slot 1 Again ---")
result2 = book_appointment("Bob", "bob@example.com", "017698765432", 1)
print(result2)  #should print "This slot is already booked"

print("\n--- Available Slots After Booking ---")
slots_after = get_available_slots()
print(slots_after)  #should show only 2 remaining slots
