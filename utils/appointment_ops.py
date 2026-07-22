from utils.db_manager import HospitalDB


class AppointmentManager:

    def __init__(self, db):
        self.db = HospitalDB(db)

    def book_appointment(self, patient_id, doctor_id, date, time, reason):
        self.db.book_appointment(patient_id, doctor_id, date, time, reason)

    def view_appointments(self):
        appointments = self.db.get_appointments()

        if not appointments:
            print("\nNo appointments found.")
            return

        print("\nAppointments")
        print("-" * 90)
        print(f"{'ID':<5}{'Patient':<20}{'Doctor':<20}{'Date':<12}{'Time':<8}{'Status'}")

        for appointment in appointments:
            print(
                f"{appointment['appointment_id']:<5}"
                f"{appointment['patient_name']:<20}"
                f"{appointment['doctor_name']:<20}"
                f"{appointment['appointment_date']:<12}"
                f"{appointment['appointment_time']:<8}"
                f"{appointment['status']}"
            )

    def view_by_patient(self, patient_id):
        appointments = self.db.get_patient_appointments(patient_id)

        if not appointments:
            print("No appointments found.")
            return

        for appointment in appointments:
            print(
                f"{appointment['appointment_date']} "
                f"{appointment['appointment_time']} "
                f"{appointment['doctor_name']} "
                f"{appointment['status']}"
            )

    def update_status(self, appointment_id, status):
        self.db.update_appointment_status(appointment_id, status)