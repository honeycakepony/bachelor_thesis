import sqlite3
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURR_DIR, 'pdp_source_1.db')

lookup = 'SELECT ip_address FROM subjects WHERE id=? AND ip_address=?'
param_1 = 'ethan@mission−thesis.org'
param_2 = '217.233.97.120'

def _lookup_valid_entry_2_params(query: str, param_1: str, param_2: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, (param_1, param_2))
    if c.fetchone() is not None:
        conn.close()
        return True
    return False

if __name__ == '__main__':
    print(_lookup_valid_entry_2_params(lookup, param_1, param_2))