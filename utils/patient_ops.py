"""
patient_ops.py — Patient management operations.
"""

import sqlite3

from utils.db_manager import HospitalDB


class Person:
    """Base class for all entities."""

    def __init__(self, name: str):
        self.name = name

    def describe(self) -> str:
        return f'Person: {self.name}'


class Patient(Person):
    """Represents a registered patient loaded from the DB."""

    def __init__(self, patient_id: int, name: str, dob: str, phone: str, blood_type: str, ward: str):
        super().__init__(name)
        self.id = patient_id
        self.dob = dob
        self.phone = phone
        self.blood_type = blood_type
        self.ward = ward

    def describe(self) -> str:
        return (f'[Patient ID: {self.id}] {self.name} | '
                f'DOB: {self.dob} | Phone: {self.phone} | '
                f'Blood Type: {self.blood_type} | Ward: {self.ward}')


class PatientManager(HospitalDB):
    """Handles all patient-related database operations."""

    VALID_FIELDS = {'name', 'dob', 'phone', 'blood_type', 'ward'}

    def add_patient(self, name: str, dob: str, phone: str, blood_type: str, ward: str) -> None:
        """Register a new patient and occupy a bed in the given ward."""
        if not name:
            print('Error: Patient name is required.')
            return

        try:
            with self._conn() as c:
                ward_row = c.execute('SELECT * FROM wards WHERE name = ?', (ward,)).fetchone()
                if not ward_row:
                    print(f'Error: Ward "{ward}" does not exist.')
                    return
                if ward_row['occupied'] >= ward_row['capacity']:
                    print(f'Error: Ward "{ward}" is full. No beds available.')
                    return

                c.execute(
                    'INSERT INTO patients (name, dob, phone, blood_type, ward) VALUES (?, ?, ?, ?, ?)',
                    (name.strip().title(), dob.strip(), phone.strip(), blood_type.strip().upper(), ward.strip())
                )
                c.execute('UPDATE wards SET occupied = occupied + 1 WHERE name = ?', (ward,))
            print(f'Patient "{name.title()}" successfully registered.')
        except sqlite3.Error as e:
            print(f'Error adding patient: {e}')

    def view_patients(self):
        """Display all patients and return them as Patient objects."""
        try:
            with self._conn() as c:
                rows = c.execute('SELECT * FROM patients ORDER BY id').fetchall()

            if not rows:
                print('No patient files found.')
                return []

            patients = [Patient(r['id'], r['name'], r['dob'], r['phone'], r['blood_type'], r['ward']) for r in rows]
            print(f'\n--- Active Patient Profiles ({len(patients)}) ---')
            for p in patients:
                print(p.describe())
            return patients
        except sqlite3.Error as e:
            print(f'Error viewing patients: {e}')
            return []

    def search_patient(self, keyword: str) -> None:
        """Search patients by name, blood type, or ward."""
        if not keyword:
            print('Error: Search term cannot be blank.')
            return

        try:
            with self._conn() as c:
                rows = c.execute(
                    'SELECT * FROM patients WHERE name LIKE ? OR blood_type LIKE ? OR ward LIKE ?',
                    (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
                ).fetchall()

            if not rows:
                print(f'No patient records matched "{keyword}".')
                return

            print(f'\nFound {len(rows)} matching record(s):')
            for r in rows:
                p = Patient(r['id'], r['name'], r['dob'], r['phone'], r['blood_type'], r['ward'])
                print(p.describe())
        except sqlite3.Error as e:
            print(f'Error searching patients: {e}')

    def update_patient(self, patient_id: int, field: str, value: str) -> None:
        """Update a single field on a patient's record."""
        field = field.strip().lower()
        if field not in self.VALID_FIELDS:
            print(f'Error: "{field}" is not a valid field. Choose from {", ".join(sorted(self.VALID_FIELDS))}.')
            return

        try:
            with self._conn() as c:
                current = c.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
                if not current:
                    print(f'Patient ID {patient_id} not found.')
                    return

                # Ward changes need to move the bed allocation between wards
                if field == 'ward':
                    old_ward = current['ward']
                    new_ward = value.strip()

                    if new_ward != old_ward:
                        new_ward_row = c.execute('SELECT * FROM wards WHERE name = ?', (new_ward,)).fetchone()
                        if not new_ward_row:
                            print(f'Error: Ward "{new_ward}" does not exist.')
                            return
                        if new_ward_row['occupied'] >= new_ward_row['capacity']:
                            print(f'Error: Ward "{new_ward}" is full. Update aborted.')
                            return

                        c.execute('UPDATE wards SET occupied = MAX(0, occupied - 1) WHERE name = ?', (old_ward,))
                        c.execute('UPDATE wards SET occupied = occupied + 1 WHERE name = ?', (new_ward,))

                c.execute(f'UPDATE patients SET {field} = ? WHERE id = ?', (value.strip(), patient_id))
            print(f'Patient {patient_id} updated: {field} = "{value}".')
        except sqlite3.Error as e:
            print(f'Error updating patient: {e}')

    def delete_patient(self, patient_id: int) -> None:
        """Delete a patient record and free their ward bed."""
        try:
            with self._conn() as c:
                row = c.execute('SELECT ward, name FROM patients WHERE id = ?', (patient_id,)).fetchone()
                if not row:
                    print(f'Patient ID {patient_id} not found.')
                    return

                c.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
                c.execute('UPDATE wards SET occupied = MAX(0, occupied - 1) WHERE name = ?', (row['ward'],))
            print(f'Patient "{row["name"]}" discharged; bed in {row["ward"]} freed.')
        except sqlite3.Error as e:
            print(f'Error deleting patient: {e}')