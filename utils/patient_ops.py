import sqlite3

from utils.db_manager import HospitalDB 


db_manager = HospitalDB()



class Person:
    #The base class for all the etities
    def __init__(self, name: str):
        self.name = name

    def describe(self) -> str:
        
        return f"Person: {self.name}"

#Subclass-Represents the registered patient from the DB
class Patient(Person):
   
    def __init__(self, patient_id: int, name: str, dob: str, phone: str, blood_type: str, ward: str):
        super().__init__(name)  
        self.id = patient_id
        self.dob = dob
        self.phone = phone
        self.blood_type = blood_type
        self.ward = ward
#The custom patient details
    def describe(self) -> str:
        return (f"[Patient ID: {self.id}] {self.name} | "
                f"DOB: {self.dob} | Phone: {self.phone} | "
                f"Blood Type: {self.blood_type} | Ward: {self.ward}")



# PATIENT CRUD & SEARCH OPERATIONS

#Register the patients
def register_patient():
    
    print("\n--- Register New Patient ---")
    name = input("Enter Full Name: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    phone = input("Enter Phone Number: ").strip()
    blood_type = input("Enter Blood Type: ").strip()
    ward = input("Assign Ward Name: ").strip()

    if not name:
        print("Error: Patient name is required.")
        return

    try:
        with db_manager._conn() as conn:
            cursor = conn.cursor()
            
            
            cursor.execute("SELECT available_beds FROM wards WHERE name = ?", (ward,))
            ward_res = cursor.fetchone()
            if not ward_res or ward_res['available_beds'] <= 0:
                print("[-] Error: Designated Ward is either full or doesn't exist.")
                return

            
            cursor.execute(
                "INSERT INTO patients (name, dob, phone, blood_type, ward) VALUES (?, ?, ?, ?, ?)",
                (name, dob, phone, blood_type, ward)
            )
            # Deduct a bed from the ward inventory
            cursor.execute("UPDATE wards SET available_beds = available_beds - 1 WHERE name = ?", (ward,))
            conn.commit()
            print(f"[+] Patient '{name}' successfully registered!")
    except sqlite3.Error as e:
        print(f"[-] Database Error: {e}")


def view_patients():
    """Read/View all patient records using the polymorphic describe method."""
    print("\n--- Active Patient Profiles ---")
    try:
        with db_manager._conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            
            if not rows:
                print("No patient files found.")
                return
                
            for r in rows:
                # Instantiate OOP object using sqlite3.Row dictionary keys
                p = Patient(r['id'], r['name'], r['dob'], r['phone'], r['blood_type'], r['ward'])
                # Call polymorphic describe method
                print(p.describe())
    except sqlite3.Error as e:
        print(f"[-] Database Error: {e}")


def search_patient():
    """Search for patient records by name or ward assignment."""
    print("\n--- Search Patient Records ---")
    search_term = input("Enter Patient Name or Ward to search: ").strip()
    
    if not search_term:
        print("[-] Search term cannot be blank.")
        return

    try:
        with db_manager._conn() as conn:
            cursor = conn.cursor()
            # Dynamic query searching via partial matching (LIKE) on Name or Ward
            cursor.execute(
                "SELECT * FROM patients WHERE name LIKE ? OR ward LIKE ?", 
                (f"%{search_term}%", f"%{search_term}%")
            )
            rows = cursor.fetchall()
            
            if not rows:
                print(f"[-] No patient records matched '{search_term}'.")
                return
                
            print(f"\n[+] Found {len(rows)} matching record(s):")
            for r in rows:
                p = Patient(r['id'], r['name'], r['dob'], r['phone'], r['blood_type'], r['ward'])
                print(p.describe())
    except sqlite3.Error as e:
        print(f"[-] Database Error: {e}")


def update_patient():
    #Updating the patient's contact number and ward details based on their ID.
   
    print("\n--- Update Patient Profile ---")
    try:
        pid = int(input("Enter Patient Database ID to update: "))
        new_phone = input("Enter New Phone Number (Leave blank to keep current): ").strip()
        new_ward = input("Enter New Ward Assignment (Leave blank to keep current): ").strip()
        
        with db_manager._conn() as conn:
            cursor = conn.cursor()
            
            # Fetch current entry to evaluate modifications
            cursor.execute("SELECT * FROM patients WHERE id = ?", (pid,))
            current_patient = cursor.fetchone()
            if not current_patient:
                print("[-] Patient record not found.")
                return

            # Retain old records if inputs are empty strings
            phone_to_update = new_phone if new_phone else current_patient['phone']
            old_ward = current_patient['ward']
            ward_to_update = new_ward if new_ward else old_ward

            # Handle bed vacancy tracking if ward assignment is changing
            if new_ward and new_ward != old_ward:
                # Check new ward vacancy
                cursor.execute("SELECT available_beds FROM wards WHERE name = ?", (new_ward,))
                ward_res = cursor.fetchone()
                if not ward_res or ward_res['available_beds'] <= 0:
                    print("[-] Error: New ward is full or non-existent. Update aborted.")
                    return
                
                # Reclaim bed space from old ward, deduct from new ward
                cursor.execute("UPDATE wards SET available_beds = available_beds + 1 WHERE name = ?", (old_ward,))
                cursor.execute("UPDATE wards SET available_beds = available_beds - 1 WHERE name = ?", (new_ward,))

            cursor.execute(
                "UPDATE patients SET phone = ?, ward = ? WHERE id = ?", 
                (phone_to_update, ward_to_update, pid)
            )
            conn.commit()
            print("Patient profile successfully updated.")
            
    except ValueError:
        print("Error: ID must be a numeric integer value.")
    except sqlite3.Error as e:
        print(f"[-] Database Error: {e}")


def delete_patient():
    """Delete/Discharge a patient and free up a bed space in their assigned ward."""
    print("\n--- Discharge / Delete Patient Record ---")
    try:
        pid = int(input("Enter Patient ID to discharge: "))
        
        with db_manager._conn() as conn:
            cursor = conn.cursor()
            # Find the ward they belong to before deleting them
            cursor.execute("SELECT ward FROM patients WHERE id = ?", (pid,))
            row = cursor.fetchone()
            if not row:
                print("[-] Patient record not found.")
                return
                
            assigned_ward = row['ward']
            
            # Delete record
            cursor.execute("DELETE FROM patients WHERE id = ?", (pid,))
            # Reclaim bed space back to the ward
            cursor.execute("UPDATE wards SET available_beds = available_beds + 1 WHERE name = ?", (assigned_ward,))
            conn.commit()
            print("[+] Patient successfully discharged; ward bed reclaimed.")
    except ValueError:
        print("[-] Error: ID must be an integer value.")
    except sqlite3.Error as e:
        print(f"[-] Database Error: {e}")