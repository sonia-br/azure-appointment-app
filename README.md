# Azure Appointment Booking System

A web-based platform for booking appointments, built with **Python + Flask**, hosted on **Microsoft Azure**. Users can view time slots, make a booking, and receive confirmation emails.

---

## Features

- View available time slots
- Book an appointment
- Prevent double booking
- Receive booking confirmation via email
- Get reminder emails

---

## Team Responsibilities

| Developer | Responsibility                           | Branch                        |
|-----------|------------------------------------------|-------------------------------|
| Sofia     | Booking logic & database schema          | `feature/booking-logic`       |
| Kaan      | Flask app & route logic                  | `feature/flask-routing`       |
| Steven    | Email & Calendar integration             | `feature/email-integration`   |

---

## Git Workflow

Each developer works in their **own branch** based on their feature area.


### Commit Guidelines (Conventional Commits)

Use this format:
<type>(<scope>): <short description>

#### Examples:

| Type     | Example                                       | Purpose                        |
|----------|-----------------------------------------------|--------------------------------|
| `feat`   | `feat(booking): add slot availability check`  | New feature                    |
| `fix`    | `fix(email): correct confirmation content`    | Bug fix                        |
| `chore`  | `chore: update .gitignore for db`             | Non-feature work (e.g. setup)  |
| `docs`   | `docs: update README with team info`          | Documentation only             |
| `test`   | `test(booking): add test for double booking`  | Test code                      |

---

## Local Setup Instructions

### 1. Clone the project and install dependencies

git clone <repo-url>
cd azure-appointment-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### Create Local Database

sqlite3 booking.db < app/db_setup.sql
sqlite3 booking.db < app/test_data.sql


