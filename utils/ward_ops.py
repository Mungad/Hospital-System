"""
ward_ops.py — Ward occupancy and bed management.
"""

from utils.db_manager import HospitalDB


class WardManager(HospitalDB):
    """Handles ward occupancy tracking."""

    def view_wards(self) -> None:
        """Display ward occupancy and available beds."""
        try:
            with self._conn() as c:
                rows = c.execute('SELECT * FROM wards ORDER BY name').fetchall()
            print(f'\n  {"Ward":<14} {"Capacity":>10} {"Occupied":>10} {"Available":>10} {"Status"}')
            print('  ' + '-' * 58)
            for r in rows:
                available = r['capacity'] - r['occupied']
                status    = 'FULL' if available == 0 else ('🟡 LOW' if available <= 3 else '🟢 OK')
                print(f'  {r["name"]:<14} {r["capacity"]:>10} {r["occupied"]:>10} {available:>10}   {status}')
        except Exception as e:
            print(f'Error viewing wards: {e}')

    def admit_patient(self, ward_name: str) -> None:
        """Increment occupancy when a patient is admitted."""
        try:
            with self._conn() as c:
                row = c.execute('SELECT * FROM wards WHERE name=?', (ward_name,)).fetchone()
                if not row:
                    print(f'Ward "{ward_name}" not found.')
                    return
                if row['occupied'] >= row['capacity']:
                    print(f'{ward_name} is full. No beds available.')
                    return
                c.execute('UPDATE wards SET occupied = occupied + 1 WHERE name=?', (ward_name,))
            print(f'Patient admitted to {ward_name}.')
        except Exception as e:
            print(f'Error admitting patient: {e}')

    def discharge_patient(self, ward_name: str) -> None:
        """Decrement occupancy when a patient is discharged."""
        try:
            with self._conn() as c:
                c.execute(
                    'UPDATE wards SET occupied = MAX(0, occupied - 1) WHERE name=?',
                    (ward_name,)
                )
            print(f'Patient discharged from {ward_name}.')
        except Exception as e:
            print(f'Error discharging patient: {e}')
