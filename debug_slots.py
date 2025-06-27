import sqlite3

conn = sqlite3.connect("booking.db")
cur = conn.cursor()

print("=== All slots ===")
cur.execute("SELECT * FROM slots")
print(cur.fetchall())

print("\n=== All appointments ===")
cur.execute("SELECT * FROM appointments")
print(cur.fetchall())

print("\n=== Available slots (manual query) ===")
cur.execute("""
    SELECT * FROM slots
    WHERE id NOT IN (SELECT slot_id FROM appointments)
""")
print(cur.fetchall())

conn.close()
