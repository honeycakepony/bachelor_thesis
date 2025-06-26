import sqlite3
import re


if __name__ == '__main__':
    matches = re.findall("'([^']+)'", "['abc']['def']['hij']")
    print(f'{matches=}, {matches[-1]=}')
    exit(100)

# conn = sqlite3.connect('../data_sources/pdp_source_1.db')
# c = conn.cursor()
# c.execute("SELECT * FROM users")
# res = c.fetchall()
# print(res)
#
# id = 'ethan@mission−thesis.org'
# ip= '217.233.97.120'
# c.execute("SELECT ip_v4 FROM users WHERE id=? AND ip_v4=?", (id, ip))
# res = c.fetchall()
# print(res)
# conn.close()