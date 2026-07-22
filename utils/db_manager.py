import sqlite3


class HospitalDB:

  def __init__(self, db_name="hospital.db"):
    self.db_name = db_name
    self.create_tables()

  def connect(self):
    """Create and return a database connection with row factory enabled."""
    try:
      conn = sqlite3.connect(self.db_name)
      conn.row_factory = sqlite3.Row
      return conn
    except Exception as e:
      print(f"  ✗ Database connection error: {e}")
      return None

  def create_tables(self):
    """Create all database tables securely."""
    conn = self.connect()
    if not conn:
      return
    try:
      cursor = conn.cursor()
      cursor.executescript("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    dob TEXT,
                    phone TEXT,
                    blood_type TEXT,
                    ward TEXT
                );

                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialization TEXT,
                    department TEXT
                );

                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    doctor_id INTEGER,
                    appointment_date TEXT,
                    appointment_time TEXT,
                    reason TEXT,
                    status TEXT DEFAULT 'Scheduled',
                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
                );

                CREATE TABLE IF NOT EXISTS bills (
                    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    item TEXT,
                    amount REAL,
                    payment_status TEXT DEFAULT 'Unpaid',
                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                );

                CREATE TABLE IF NOT EXISTS wards (
                    ward_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ward_name TEXT UNIQUE,
                    total_beds INTEGER,
                    occupied_beds INTEGER DEFAULT 0
                );
            """)
      conn.commit()
    except Exception as e:
      print(f"  ✗ Error creating tables: {e}")
    finally:
      conn.close()

  # ==================== PATIENT CRUD ====================
  def add_patient(self, name, dob, phone, blood_type, ward):
    try:
      with self.connect() as conn:
        conn.execute(
            "INSERT INTO patients (name, dob, phone, blood_type, ward) VALUES"
            " (?, ?, ?, ?, ?)",
            (name, dob, phone, blood_type, ward),
        )
        conn.commit()
        print(f"  ✓ Patient {name} registered successfully.")
    except Exception as e:
      print(f"  ✗ Error adding patient: {e}")

  def get_patients(self):
    try:
      with self.connect() as conn:
        return conn.execute(
            "SELECT * FROM patients ORDER BY name"
        ).fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching patients: {e}")
      return []

  def update_patient(self, patient_id, phone, ward):
    try:
      with self.connect() as conn:
        conn.execute(
            "UPDATE patients SET phone = ?, ward = ? WHERE patient_id = ?",
            (phone, ward, patient_id),
        )
        conn.commit()
        print(f"  ✓ Patient ID {patient_id} updated.")
    except Exception as e:
      print(f"  ✗ Error updating patient: {e}")

  def delete_patient(self, patient_id):
    try:
      with self.connect() as conn:
        conn.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        print(f"  ✓ Patient ID {patient_id} deleted.")
    except Exception as e:
      print(f"  ✗ Error deleting patient: {e}")

  # ==================== DOCTOR CRUD ====================
  def add_doctor(self, name, specialization, department):
    try:
      with self.connect() as conn:
        conn.execute(
            "INSERT INTO doctors (name, specialization, department) VALUES"
            " (?, ?, ?)",
            (name, specialization, department),
        )
        conn.commit()
        print(f"  ✓ Doctor Dr. {name} added successfully.")
    except Exception as e:
      print(f"  ✗ Error adding doctor: {e}")

  def get_doctors(self):
    try:
      with self.connect() as conn:
        return conn.execute("SELECT * FROM doctors ORDER BY name").fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching doctors: {e}")
      return []

  # ==================== APPOINTMENT CRUD ====================
  def book_appointment(self, patient_id, doctor_id, date, time, reason):
    try:
      with self.connect() as conn:
        conn.execute(
            """
                    INSERT INTO appointments 
                    (patient_id, doctor_id, appointment_date, appointment_time, reason, status) 
                    VALUES (?, ?, ?, ?, ?, 'Scheduled')
                """,
            (patient_id, doctor_id, date, time, reason),
        )
        conn.commit()
        print(f"  ✓ Appointment booked for date {date} at {time}.")
    except Exception as e:
      print(f"  ✗ Error booking appointment: {e}")

  def get_appointments(self):
    try:
      with self.connect() as conn:
        return conn.execute("""
                    SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, 
                           a.appointment_date, a.appointment_time, a.reason, a.status 
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                """).fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching appointments: {e}")
      return []

  def get_patient_appointments(self, patient_id):
    """Retrieve appointments specific to a single patient."""
    try:
      with self.connect() as conn:
        return conn.execute(
            """
                    SELECT a.appointment_id, d.name AS doctor_name, 
                           a.appointment_date, a.appointment_time, a.reason, a.status 
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    WHERE a.patient_id = ?
                """,
            (patient_id,),
        ).fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching patient appointments: {e}")
      return []

  def update_appointment_status(self, appointment_id, status):
    """Update the status of an appointment (e.g., Completed, Cancelled)."""
    try:
      with self.connect() as conn:
        conn.execute(
            "UPDATE appointments SET status = ? WHERE appointment_id = ?",
            (status, appointment_id),
        )
        conn.commit()
        print(f"  ✓ Appointment ID {appointment_id} status updated to {status}.")
    except Exception as e:
      print(f"  ✗ Error updating appointment status: {e}")

  # ==================== BILLING CRUD ====================
  def generate_bill(self, patient_id, item, amount):
    try:
      with self.connect() as conn:
        conn.execute(
            "INSERT INTO bills (patient_id, item, amount, payment_status) VALUES"
            " (?, ?, ?, 'Unpaid')",
            (patient_id, item, amount),
        )
        conn.commit()
        print(
            f"  ✓ Bill item '{item}' (${amount}) generated for Patient ID"
            f" {patient_id}."
        )
    except Exception as e:
      print(f"  ✗ Error generating bill: {e}")

  def get_patient_bills(self, patient_id):
    """Retrieve all bill records for a specific patient."""
    try:
      with self.connect() as conn:
        return conn.execute(
            "SELECT * FROM bills WHERE patient_id = ?", (patient_id,)
        ).fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching patient bills: {e}")
      return []

  def get_all_bills(self):
    """Retrieve all bills across the system."""
    try:
      with self.connect() as conn:
        return conn.execute("SELECT * FROM bills").fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching all bills: {e}")
      return []

  def mark_bill_paid(self, patient_id):
    """Mark all bills belonging to a specific patient as Paid."""
    try:
      with self.connect() as conn:
        conn.execute(
            "UPDATE bills SET payment_status = 'Paid' WHERE patient_id = ?",
            (patient_id,),
        )
        conn.commit()
        print(f"  ✓ All bills for Patient ID {patient_id} marked as Paid.")
    except Exception as e:
      print(f"  ✗ Error updating payment status: {e}")

  def pay_bill(self, bill_id):
    try:
      with self.connect() as conn:
        conn.execute(
            "UPDATE bills SET payment_status = 'Paid' WHERE bill_id = ?",
            (bill_id,),
        )
        conn.commit()
        print(f"  ✓ Bill ID {bill_id} marked as Paid.")
    except Exception as e:
      print(f"  ✗ Error paying bill: {e}")

  # ==================== WARD CRUD ====================
  def add_ward(self, ward_name, total_beds):
    try:
      with self.connect() as conn:
        conn.execute(
            """
                    INSERT OR IGNORE INTO wards (ward_name, total_beds, occupied_beds) 
                    VALUES (?, ?, 0)
                """,
            (ward_name, total_beds),
        )
        conn.commit()
        print(f"  ✓ Ward {ward_name} added (or already exists).")
    except Exception as e:
      print(f"  ✗ Error adding ward: {e}")

  def get_wards(self):
    try:
      with self.connect() as conn:
        return conn.execute("SELECT * FROM wards").fetchall()
    except Exception as e:
      print(f"  ✗ Error fetching wards: {e}")
      return []