"""
Doctor Management Module

Handles doctor-related operations for the
Hospital Management System.
"""

from utils.db_manager import HospitalDB


class DoctorManager:
    """Handles all doctor management operations."""

    def __init__(self):
        """Initialize the DoctorManager."""
        self.db = HospitalDB()

    def display_doctors(self, doctors):
        """
        Display doctors in a formatted table.
        """

        if not doctors:
            print("\nNo doctors found.")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<5}{'Name':<25}{'Specialization':<25}{'Department'}")
        print("=" * 80)

        for doctor in doctors:
            print(
                f"{doctor['doctor_id']:<5}"
                f"{doctor['name']:<25}"
                f"{doctor['specialization']:<25}"
                f"{doctor['department']}"
            )

        print("=" * 80)
        print(f"Total Doctors: {len(doctors)}")

    # ---------------------------------------------------

    def add_doctor(self, name, specialization, department):
        """
        Add a doctor.
        """

        if not name.strip():
            print("Doctor name cannot be empty.")
            return

        if not specialization.strip():
            print("Specialization cannot be empty.")
            return

        if not department.strip():
            print("Department cannot be empty.")
            return

        try:

            with self.db.connect() as conn:

                conn.execute(
                    """
                    INSERT INTO doctors
                    (name, specialization, department)
                    VALUES (?, ?, ?)
                    """,
                    (name, specialization, department),
                )

                conn.commit()

                print(f"Doctor '{name}' added successfully.")

        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------------------------------

    def view_doctors(self):
        """
        Display all doctors.
        """

        try:

            with self.db.connect() as conn:

                doctors = conn.execute(
                    """
                    SELECT *
                    FROM doctors
                    ORDER BY name
                    """
                ).fetchall()

            self.display_doctors(doctors)

        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------------------------------

    def search_doctor_by_name(self, name):
        """
        Search doctor by name.
        """

        if not name.strip():
            print("Doctor name cannot be empty.")
            return

        try:

            with self.db.connect() as conn:

                doctors = conn.execute(
                    """
                    SELECT *
                    FROM doctors
                    WHERE name LIKE ?
                    ORDER BY name
                    """,
                    (f"%{name}%",),
                ).fetchall()

            self.display_doctors(doctors)

        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------------------------------

    def search_doctor_by_department(self, department):
        """
        Search doctors by department.
        """

        if not department.strip():
            print("Department cannot be empty.")
            return

        try:

            with self.db.connect() as conn:

                doctors = conn.execute(
                    """
                    SELECT *
                    FROM doctors
                    WHERE department LIKE ?
                    ORDER BY name
                    """,
                    (f"%{department}%",),
                ).fetchall()

            self.display_doctors(doctors)

        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------------------------------

    def update_doctor(self, doctor_id, name, specialization, department):
        """
        Update doctor information.
        """

        if not name.strip():
            print("Doctor name cannot be empty.")
            return

        if not specialization.strip():
            print("Specialization cannot be empty.")
            return

        if not department.strip():
            print("Department cannot be empty.")
            return

        try:

            with self.db.connect() as conn:

                doctor = conn.execute(
                    """
                    SELECT *
                    FROM doctors
                    WHERE doctor_id=?
                    """,
                    (doctor_id,),
                ).fetchone()

                if doctor is None:
                    print("Doctor not found.")
                    return

                conn.execute(
                    """
                    UPDATE doctors
                    SET
                        name=?,
                        specialization=?,
                        department=?
                    WHERE doctor_id=?
                    """,
                    (
                        name,
                        specialization,
                        department,
                        doctor_id,
                    ),
                )

                conn.commit()

                print("Doctor updated successfully.")

        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------------------------------

    def delete_doctor(self, doctor_id):
        """
        Delete doctor.
        """

        try:

            with self.db.connect() as conn:

                doctor = conn.execute(
                    """
                    SELECT *
                    FROM doctors
                    WHERE doctor_id=?
                    """,
                    (doctor_id,),
                ).fetchone()

                if doctor is None:
                    print("Doctor not found.")
                    return

                conn.execute(
                    """
                    DELETE FROM doctors
                    WHERE doctor_id=?
                    """,
                    (doctor_id,),
                )

                conn.commit()

                print(f"Doctor '{doctor['name']}' deleted successfully.")

        except Exception as e:
            print(f"Error: {e}")