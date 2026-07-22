# Hospital Management System

## Description
Console-based Hospital Management System built with OOP design and SQLite persistence.
Developed as a Mid-Term Project for FAC Academy — Python & Django Programme.

## Features
- **Patient Registration** — Add, view, search, update, delete patients
- **Doctor Management** — Add, view, search, delete doctors by name/department
- **Appointment System** — Book, view, update appointment status
- **Billing System** — Add bill items, print invoices, mark as paid
- **Ward Management** — Track occupancy, admit/discharge patients

## Project Structure
```
hospital_system/
├── main.py                  ← Menu loop and user interaction
├── hospital.db              ← SQLite database (auto-created)
├── README.md
├── requirements.txt
├── .gitignore
└── utils/
    ├── __init__.py
    ├── db_manager.py        ← HospitalDB base class
    ├── patient_ops.py       ← Patient CRUD
    ├── doctor_ops.py        ← Doctor management
    ├── appointment_ops.py   ← Appointment booking
    ├── billing.py           ← Invoice generation
    └── ward_ops.py          ← Ward occupancy
```

## Setup
```bash
git clone <your-github-url>
cd hospital_system
python main.py
```

## Tech Stack
Python 3.12 | SQLite3 | OOP (Inheritance, Encapsulation, Polymorphism)

## OOP Design
- `HospitalDB` — Base class (database connection, table init)
- `PatientManager(HospitalDB)` — Inherits DB, adds patient operations
- `DoctorManager(HospitalDB)` — Inherits DB, adds doctor operations
- `AppointmentManager(HospitalDB)` — Inherits DB, adds appointment operations
- `BillingManager(HospitalDB)` — Inherits DB, adds billing operations
- `WardManager(HospitalDB)` — Inherits DB, adds ward operations
