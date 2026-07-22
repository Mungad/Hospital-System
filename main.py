from utils.db_manager import HospitalDB

# Initialize database and tables
db = HospitalDB()
print("--- TESTING DATABASE OPERATIONS ---")

# 1. Test Wards & Doctors
db.add_ward("ICU", 10)
db.add_doctor("Dr. House", "Diagnostics", "Internal Medicine")

# 2. Test Patients CRUD
db.add_patient("John Doe", "1990-01-15", "555-0100", "A+", "ICU")
patients = db.get_patients()
if patients:
  print(f"Successfully retrieved {len(patients)} patient(s).")

# 3. Test Appointments
if patients:
  p_id = patients[0]["patient_id"]
  db.book_appointment(p_id, 1, "2026-07-01", "10:30 AM", "Routine Checkup")

# 4. Test Billing
if patients:
  db.generate_bill(p_id, 250.00)

print("\n--- DATABASE TESTS COMPLETED SUCCESSFULLY ---")