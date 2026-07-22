"""
Hospital Management System
FAC Academy | Mid-Term Project

Run: python3 main.py
"""

from utils.patient_ops     import PatientManager
from utils.doctor_ops      import DoctorManager
from utils.appointment_ops import AppointmentManager
from utils.billing     import BillingManager
from utils.ward_ops        import WardManager

# Single shared DB file for all managers
DB = 'hospital.db'
pm = PatientManager(DB)
dm = DoctorManager(DB)
am = AppointmentManager(DB)
bm = BillingManager(DB)
wm = WardManager(DB)


# Sub-menus

def patient_menu() -> None:
    while True:
        print('\n--- Patient Management ---')
        print('  1. Register Patient')
        print('  2. View All Patients')
        print('  3. Search Patient')
        print('  4. Update Patient')
        print('  5. Delete Patient')
        print('  0. Back')
        ch = input('  Select: ').strip()

        if ch == '1':
            name       = input('  Name       : ').strip()
            dob        = input('  DOB (YYYY-MM-DD): ').strip()
            phone      = input('  Phone      : ').strip()
            blood_type = input('  Blood Type : ').strip()
            ward       = input('  Ward       : ').strip()
            pm.add_patient(name, dob, phone, blood_type, ward)

        elif ch == '2':
            pm.view_patients()

        elif ch == '3':
            keyword = input('  Search (name/blood type): ').strip()
            pm.search_patient(keyword)

        elif ch == '4':
            pm.view_patients()
            try:
                pid   = int(input('  Patient ID to update: '))
                field = input('  Field (name/dob/phone/blood_type/ward): ').strip()
                value = input(f'  New {field}: ').strip()
                pm.update_patient(pid, field, value)
            except ValueError:
                print('Invalid ID.')

        elif ch == '5':
            pm.view_patients()
            try:
                pid = int(input('  Patient ID to delete: '))
                confirm = input(f'  Confirm delete patient {pid}? (yes/no): ').strip().lower()
                if confirm == 'yes':
                    pm.delete_patient(pid)
            except ValueError:
                print('Invalid ID.')

        elif ch == '0':
            break


def doctor_menu() -> None:
    while True:
        print('\n--- Doctor Management ---')
        print('  1. Add Doctor')
        print('  2. View All Doctors')
        print('  3. Search Doctor')
        print('  4. Delete Doctor')
        print('  0. Back')
        ch = input('  Select: ').strip()

        if ch == '1':
            name           = input('  Name           : ').strip()
            specialisation = input('  Specialisation : ').strip()
            department     = input('  Department     : ').strip()
            dm.add_doctor(name, specialisation, department)

        elif ch == '2':
            dm.view_doctors()

        elif ch == '3':
            keyword = input('  Search (name/department): ').strip()
            dm.search_doctor(keyword)

        elif ch == '4':
            dm.view_doctors()
            try:
                did = int(input('  Doctor ID to delete: '))
                confirm = input(f'  Confirm delete doctor {did}? (yes/no): ').strip().lower()
                if confirm == 'yes':
                    dm.delete_doctor(did)
            except ValueError:
                print('Invalid ID.')

        elif ch == '0':
            break


def appointment_menu() -> None:
    while True:
        print('\n--- Appointment System ---')
        print('  1. Book Appointment')
        print('  2. View All Appointments')
        print('  3. View by Patient')
        print('  4. Update Appointment Status')
        print('  0. Back')
        ch = input('  Select: ').strip()

        if ch == '1':
            pm.view_patients()
            dm.view_doctors()
            try:
                pid    = int(input('  Patient ID : '))
                did    = int(input('  Doctor ID  : '))
                date   = input('  Date (YYYY-MM-DD): ').strip()
                time   = input('  Time (HH:MM)     : ').strip()
                reason = input('  Reason           : ').strip()
                am.book_appointment(pid, did, date, time, reason)
            except ValueError:
                print('Invalid ID.')

        elif ch == '2':
            am.view_appointments()

        elif ch == '3':
            try:
                pid = int(input('  Patient ID: '))
                am.view_by_patient(pid)
            except ValueError:
                print('Invalid ID.')

        elif ch == '4':
            am.view_appointments()
            try:
                aid    = int(input('  Appointment ID: '))
                status = input('  New Status (Scheduled/Completed/Cancelled): ').strip()
                am.update_status(aid, status)
            except ValueError:
                print('Invalid ID.')

        elif ch == '0':
            break


def billing_menu() -> None:
    while True:
        print('\n--- Billing System ---')
        print('  1. Add Bill Item')
        print('  2. Print Invoice')
        print('  3. Mark Bills as Paid')
        print('  4. View All Bills Summary')
        print('  0. Back')
        ch = input('  Select: ').strip()

        if ch == '1':
            pm.view_patients()
            try:
                pid    = int(input('  Patient ID : '))
                item   = input('  Item       : ').strip()
                amount = float(input('  Amount (KES): '))
                bm.add_bill_item(pid, item, amount)
            except ValueError:
                print('Invalid input.')

        elif ch == '2':
            try:
                pid = int(input('  Patient ID: '))
                bm.print_invoice(pid)
            except ValueError:
                print('Invalid ID.')

        elif ch == '3':
            try:
                pid = int(input('  Patient ID: '))
                bm.mark_paid(pid)
            except ValueError:
                print('Invalid ID.')

        elif ch == '4':
            bm.view_all_bills()

        elif ch == '0':
            break


def ward_menu() -> None:
    while True:
        print('\n--- Ward Management ---')
        print('  1. View Ward Occupancy')
        print('  2. Admit Patient to Ward')
        print('  3. Discharge Patient from Ward')
        print('  0. Back')
        ch = input('  Select: ').strip()

        if ch == '1':
            wm.view_wards()

        elif ch == '2':
            wm.view_wards()
            ward = input('  Ward name: ').strip()
            wm.admit_patient(ward)

        elif ch == '3':
            wm.view_wards()
            ward = input('  Ward name: ').strip()
            wm.discharge_patient(ward)

        elif ch == '0':
            break


#  Main Menu

def main() -> None:
    print('\n' + '=' * 50)
    print('       HOSPITAL MANAGEMENT SYSTEM')
    print('       FAC Academy | Python Mid-Term Project')
    print('=' * 50)

    while True:
        print('\n====== MAIN MENU ======')
        print('  1. Patient Registration')
        print('  2. Doctor Management')
        print('  3. Appointment System')
        print('  4. Billing System')
        print('  5. Ward Management')
        print('  0. Exit')
        print('=======================')
        ch = input('  Select: ').strip()

        if   ch == '1': patient_menu()
        elif ch == '2': doctor_menu()
        elif ch == '3': appointment_menu()
        elif ch == '4': billing_menu()
        elif ch == '5': ward_menu()
        elif ch == '0':
            print('\n  Goodbye! System closed.\n')
            break
        else:
            print('Invalid choice. Enter 0-5.')


if __name__ == '__main__':
    main()
