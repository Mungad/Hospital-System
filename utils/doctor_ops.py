"""
doctor_ops.py — Doctor management operations.
"""

from utils.db_manager import HospitalDB


class DoctorManager(HospitalDB):
    """Handles all doctor-related database operations."""

    def add_doctor(self, name: str, specialisation: str, department: str) -> None:
        """Add a new doctor."""
        try:
            with self._conn() as c:
                c.execute(
                    'INSERT INTO doctors VALUES (NULL,?,?,?)',
                    (name.strip().title(), specialisation.strip(), department.strip().title())
                )
            print(f'Dr. "{name.title()}" added successfully.')
        except Exception as e:
            print(f'Error adding doctor: {e}')

    def view_doctors(self) -> None:
        """Display all doctors in a formatted table."""
        try:
            with self._conn() as c:
                rows = c.execute(
                    'SELECT * FROM doctors ORDER BY name'
                ).fetchall()
            if not rows:
                print('  No doctors registered yet.')
                return
            print(f'\n  {"ID":>4}  {"Name":<24} {"Specialisation":<22} {"Department"}')
            print('  ' + '-' * 65)
            for r in rows:
                print(f'  {r["id"]:>4}  {r["name"]:<24} {r["specialisation"]:<22} {r["department"]}')
            print(f'\n  Total: {len(rows)} doctor(s)')
        except Exception as e:
            print(f'Error viewing doctors: {e}')

    def search_doctor(self, keyword: str) -> None:
        """Search doctors by name or department."""
        try:
            with self._conn() as c:
                rows = c.execute(
                    'SELECT * FROM doctors WHERE name LIKE ? OR department LIKE ? OR specialisation LIKE ?',
                    (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
                ).fetchall()
            if not rows:
                print(f'  No doctors matching "{keyword}".')
                return
            print(f'\n  Found {len(rows)} result(s):')
            print(f'  {"ID":>4}  {"Name":<24} {"Specialisation":<22} {"Department"}')
            print('  ' + '-' * 65)
            for r in rows:
                print(f'  {r["id"]:>4}  {r["name"]:<24} {r["specialisation"]:<22} {r["department"]}')
        except Exception as e:
            print(f'Error searching doctors: {e}')

    def delete_doctor(self, doctor_id: int) -> None:
        """Delete a doctor record."""
        try:
            with self._conn() as c:
                row = c.execute(
                    'SELECT name FROM doctors WHERE id = ?', (doctor_id,)
                ).fetchone()
                if not row:
                    print(f'Doctor ID {doctor_id} not found.')
                    return
                c.execute('DELETE FROM doctors WHERE id = ?', (doctor_id,))
            print(f'Dr. "{row["name"]}" removed.')
        except Exception as e:
            print(f'Error deleting doctor: {e}')
