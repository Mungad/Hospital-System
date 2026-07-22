"""
Ward Management Module

Handles ward operations for the
Hospital Management System.
"""

from utils.db_manager import HospitalDB


class WardManager:
    """Handles ward management operations."""

    def __init__(self):
        self.db = HospitalDB()

    # =====================================================
    # Wrapper Methods
    # =====================================================

    def add_ward(self, ward_name, total_beds):
        """
        Add a new ward using HospitalDB.
        """
        self.db.add_ward(ward_name, total_beds)

    def get_wards(self):
        """
        Return all wards from the database.
        """
        return self.db.get_wards()

    # =====================================================
    # Display Methods
    # =====================================================

    def display_wards(self, wards):
        """
        Display all wards in a formatted table.
        """

        if not wards:
            print("\nNo wards found.")
            return

        print("\n" + "=" * 75)
        print(f"{'ID':<5}{'Ward':<20}{'Total Beds':<15}{'Occupied':<15}{'Available'}")
        print("=" * 75)

        for ward in wards:

            available = ward["total_beds"] - ward["occupied_beds"]

            print(
                f"{ward['ward_id']:<5}"
                f"{ward['ward_name']:<20}"
                f"{ward['total_beds']:<15}"
                f"{ward['occupied_beds']:<15}"
                f"{available}"
            )

        print("=" * 75)

    def view_wards(self):
        """
        Display all wards.
        """
        wards = self.get_wards()
        self.display_wards(wards)

    # =====================================================
    # Ward Operations
    # =====================================================

    def admit_patient(self, ward_id):

        try:

            with self.db.connect() as conn:

                ward = conn.execute(
                    """
                    SELECT *
                    FROM wards
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                ).fetchone()

                if ward is None:
                    print("Ward not found.")
                    return

                if ward["occupied_beds"] >= ward["total_beds"]:
                    print("Ward is full.")
                    return

                conn.execute(
                    """
                    UPDATE wards
                    SET occupied_beds = occupied_beds + 1
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                )

                conn.commit()

                print("Patient admitted successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def discharge_patient(self, ward_id):

        try:

            with self.db.connect() as conn:

                ward = conn.execute(
                    """
                    SELECT *
                    FROM wards
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                ).fetchone()

                if ward is None:
                    print("Ward not found.")
                    return

                if ward["occupied_beds"] == 0:
                    print("Ward has no admitted patients.")
                    return

                conn.execute(
                    """
                    UPDATE wards
                    SET occupied_beds = occupied_beds - 1
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                )

                conn.commit()

                print("Patient discharged successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def update_ward(self, ward_id, ward_name, total_beds):

        if not ward_name.strip():
            print("Ward name cannot be empty.")
            return

        if total_beds <= 0:
            print("Total beds must be greater than zero.")
            return

        try:

            with self.db.connect() as conn:

                ward = conn.execute(
                    """
                    SELECT *
                    FROM wards
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                ).fetchone()

                if ward is None:
                    print("Ward not found.")
                    return

                if total_beds < ward["occupied_beds"]:
                    print("Total beds cannot be less than occupied beds.")
                    return

                conn.execute(
                    """
                    UPDATE wards
                    SET ward_name = ?,
                        total_beds = ?
                    WHERE ward_id = ?
                    """,
                    (ward_name, total_beds, ward_id)
                )

                conn.commit()

                print("Ward updated successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def delete_ward(self, ward_id):

        try:

            with self.db.connect() as conn:

                ward = conn.execute(
                    """
                    SELECT *
                    FROM wards
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                ).fetchone()

                if ward is None:
                    print("Ward not found.")
                    return

                if ward["occupied_beds"] > 0:
                    print("Cannot delete a ward with admitted patients.")
                    return

                conn.execute(
                    """
                    DELETE FROM wards
                    WHERE ward_id = ?
                    """,
                    (ward_id,)
                )

                conn.commit()

                print("Ward deleted successfully.")

        except Exception as e:
            print(f"Error: {e}")

    def view_available_beds(self):

        wards = self.get_wards()

        if not wards:
            print("No wards found.")
            return

        print("\nAvailable Beds")
        print("-" * 40)

        for ward in wards:

            available = ward["total_beds"] - ward["occupied_beds"]

            print(
                f"{ward['ward_name']}: "
                f"{available} bed(s) available"
            )