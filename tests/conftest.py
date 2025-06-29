import pytest
import sqlite3
import tempfile
import os
from app import booking_service

@pytest.fixture
def setup_test_db(tmp_path):
    
    db_path = tmp_path / "test_booking.db"

    booking_service.connect_db = lambda: sqlite3.connect(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.executescript("""
                         
        DROP TABLE IF EXISTS appointments;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS slots;
        
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            mobile_number TEXT NOT NULL
        );
        CREATE TABLE slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time DATETIME UNIQUE NOT NULL
        );
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (slot_id) REFERENCES slots(id),
            UNIQUE (slot_id)
        );

        INSERT INTO slots (time) VALUES 
        ('2025-07-10 12:00:00'),
        ('2025-07-11 14:00:00'),
        ('2025-07-12 16:00:00');
    """)
    connection.commit()
    connection.close()

    yield
