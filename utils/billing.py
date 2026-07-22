"""
Billing Management Module
FAC Academy | Mid-Term Project
"""

from utils.db_manager import HospitalDB


class BillingManager:
    """Handles billing operations."""

    def __init__(self, db):
        self.db = HospitalDB(db)

    def add_bill_item(self, patient_id, item, amount):
        """
        Add a bill item for a patient.
        """

        self.db.generate_bill(patient_id, item, amount)

    def print_invoice(self, patient_id):
        """
        Display a patient's invoice.
        """

        bills = self.db.get_patient_bills(patient_id)

        if not bills:
            print("\nNo bill found for this patient.")
            return

        total = 0

        print("\n" + "=" * 50)
        print("              HOSPITAL INVOICE")
        print("=" * 50)
        print(f"Patient ID : {patient_id}")
        print("-" * 50)
        print(f"{'Item':<25}{'Amount (KES)':>15}")
        print("-" * 50)

        for bill in bills:
            print(f"{bill['item']:<25}{bill['amount']:>15.2f}")
            total += bill["amount"]

        print("-" * 50)
        print(f"{'TOTAL':<25}{total:>15.2f}")
        print(f"Payment Status : {bills[0]['payment_status']}")
        print("=" * 50)

    def mark_paid(self, patient_id):
        """
        Mark all bills belonging to a patient as paid.
        """

        self.db.mark_bill_paid(patient_id)

    def view_all_bills(self):
        """
        Display all bills.
        """

        bills = self.db.get_all_bills()

        if not bills:
            print("\nNo bills found.")
            return

        print("\n" + "=" * 75)
        print("                     BILLING SUMMARY")
        print("=" * 75)

        print(
            f"{'Bill ID':<10}"
            f"{'Patient ID':<12}"
            f"{'Item':<25}"
            f"{'Amount':<12}"
            f"{'Status'}"
        )

        print("-" * 75)

        for bill in bills:
            print(
                f"{bill['bill_id']:<10}"
                f"{bill['patient_id']:<12}"
                f"{bill['item']:<25}"
                f"{bill['amount']:<12.2f}"
                f"{bill['payment_status']}"
            )