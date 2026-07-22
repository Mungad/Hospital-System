"""
db_manager.py — HospitalDB: SQLite connection and table initialisation.
All tables are created here; other modules import and use this class.
"""

import sqlite3


class HospitalDB:
    """Core database manager for the Hospital Management System."""

    def __init__(self, db: str = 'hospital.db'):
        self.db = db
        self._init_tables()

    # Connection helper
    def _conn(self) -> sqlite3.Connection:
        """Return a connection with Row factory enabled."""
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    # Table initialisation
    def _init_tables(self) -> None:
        """Create all tables if they do not exist."""
        with self._conn() as c:
            c.executescript('''
                CREATE TABLE IF NOT EXISTS patients (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    name       TEXT    NOT NULL,
                    dob        TEXT,
                    phone      TEXT,
                    blood_type TEXT,
                    ward       TEXT
                );

                CREATE TABLE IF NOT EXISTS doctors (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    name           TEXT NOT NULL,
                    specialisation TEXT,
                    department     TEXT
                );

                CREATE TABLE IF NOT EXISTS appointments (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER REFERENCES patients(id),
                    doctor_id  INTEGER REFERENCES doctors(id),
                    date       TEXT,
                    time       TEXT,
                    reason     TEXT,
                    status     TEXT DEFAULT "Scheduled"
                );

                CREATE TABLE IF NOT EXISTS bills (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER REFERENCES patients(id),
                    item       TEXT    NOT NULL,
                    amount     REAL    NOT NULL,
                    paid       INTEGER DEFAULT 0,
                    created_at TEXT    DEFAULT CURRENT_DATE
                );

                CREATE TABLE IF NOT EXISTS wards (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    name      TEXT    NOT NULL UNIQUE,
                    capacity  INTEGER NOT NULL,
                    occupied  INTEGER DEFAULT 0
                );
            ''')
            # Seed default wards if empty
            existing = c.execute('SELECT COUNT(*) FROM wards').fetchone()[0]
            if existing == 0:
                c.executemany(
                    'INSERT INTO wards (name, capacity) VALUES (?, ?)',
                    [('Ward A', 20), ('Ward B', 15), ('Ward C', 10),
                     ('ICU', 8),     ('Maternity', 12)]
                )

    # Appointment operations
    def book_appointment(self, patient_id: int, doctor_id: int,
                          date: str, time: str, reason: str) -> None:
        """Insert a new appointment record."""
        try:
            with self._conn() as c:
                # Validate patient & doctor exist first
                p = c.execute('SELECT id FROM patients WHERE id=?', (patient_id,)).fetchone()
                d = c.execute('SELECT id FROM doctors WHERE id=?', (doctor_id,)).fetchone()
                if not p:
                    print(f'Patient ID {patient_id} not found.')
                    return
                if not d:
                    print(f'Doctor ID {doctor_id} not found.')
                    return
                c.execute(
                    'INSERT INTO appointments (patient_id, doctor_id, date, time, reason) '
                    'VALUES (?, ?, ?, ?, ?)',
                    (patient_id, doctor_id, date, time, reason)
                )
            print('Appointment booked successfully.')
        except sqlite3.Error as e:
            print(f'Error booking appointment: {e}')

    def get_appointments(self):
        """Return all appointments joined with patient & doctor names."""
        try:
            with self._conn() as c:
                rows = c.execute('''
                    SELECT a.id            AS appointment_id,
                           p.name          AS patient_name,
                           d.name          AS doctor_name,
                           a.date          AS appointment_date,
                           a.time          AS appointment_time,
                           a.status        AS status
                    FROM appointments a
                    LEFT JOIN patients p ON a.patient_id = p.id
                    LEFT JOIN doctors  d ON a.doctor_id  = d.id
                    ORDER BY a.date, a.time
                ''').fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Error fetching appointments: {e}')
            return []

    def get_patient_appointments(self, patient_id: int):
        """Return appointments for a single patient, joined with doctor name."""
        try:
            with self._conn() as c:
                rows = c.execute('''
                    SELECT a.id            AS appointment_id,
                           d.name          AS doctor_name,
                           a.date          AS appointment_date,
                           a.time          AS appointment_time,
                           a.status        AS status
                    FROM appointments a
                    LEFT JOIN doctors d ON a.doctor_id = d.id
                    WHERE a.patient_id = ?
                    ORDER BY a.date, a.time
                ''', (patient_id,)).fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Error fetching patient appointments: {e}')
            return []

    def update_appointment_status(self, appointment_id: int, status: str) -> None:
        """Update the status of an appointment."""
        try:
            with self._conn() as c:
                row = c.execute('SELECT id FROM appointments WHERE id=?', (appointment_id,)).fetchone()
                if not row:
                    print(f'Appointment ID {appointment_id} not found.')
                    return
                c.execute('UPDATE appointments SET status=? WHERE id=?', (status, appointment_id))
            print(f'Appointment {appointment_id} status updated to "{status}".')
        except sqlite3.Error as e:
            print(f'Error updating appointment status: {e}')

    # Billing operations
    def generate_bill(self, patient_id: int, item: str, amount: float) -> None:
        """Add a new bill item for a patient."""
        try:
            with self._conn() as c:
                p = c.execute('SELECT id FROM patients WHERE id=?', (patient_id,)).fetchone()
                if not p:
                    print(f'Patient ID {patient_id} not found.')
                    return
                c.execute(
                    'INSERT INTO bills (patient_id, item, amount) VALUES (?, ?, ?)',
                    (patient_id, item, amount)
                )
            print(f'Bill item "{item}" ({amount:.2f}) added for patient {patient_id}.')
        except sqlite3.Error as e:
            print(f'Error generating bill: {e}')

    def get_patient_bills(self, patient_id: int):
        """Return all bill items for a patient, with a readable payment status."""
        try:
            with self._conn() as c:
                rows = c.execute('''
                    SELECT id                                        AS bill_id,
                           patient_id,
                           item,
                           amount,
                           CASE WHEN paid = 1 THEN 'Paid' ELSE 'Unpaid' END AS payment_status
                    FROM bills
                    WHERE patient_id = ?
                    ORDER BY id
                ''', (patient_id,)).fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Error fetching patient bills: {e}')
            return []

    def mark_bill_paid(self, patient_id: int) -> None:
        """Mark all bills belonging to a patient as paid."""
        try:
            with self._conn() as c:
                result = c.execute('UPDATE bills SET paid = 1 WHERE patient_id = ?', (patient_id,))
                if result.rowcount == 0:
                    print(f'No bills found for patient {patient_id}.')
                    return
            print(f'All bills for patient {patient_id} marked as paid.')
        except sqlite3.Error as e:
            print(f'Error marking bills as paid: {e}')

    def get_all_bills(self):
        """Return every bill in the system, with a readable payment status."""
        try:
            with self._conn() as c:
                rows = c.execute('''
                    SELECT id                                        AS bill_id,
                           patient_id,
                           item,
                           amount,
                           CASE WHEN paid = 1 THEN 'Paid' ELSE 'Unpaid' END AS payment_status
                    FROM bills
                    ORDER BY id
                ''').fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Error fetching all bills: {e}')
            return []