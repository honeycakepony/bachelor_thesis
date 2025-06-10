import sqlite3

conn = sqlite3.connect('pdp_source_1.db')
c = conn.cursor()
c.execute("SELECT * FROM users")
res = c.fetchall()
print(res)

id = 'ethan@mission−thesis.org'
ip= '217.233.97.120'
c.execute("SELECT ip_v4 FROM users WHERE id=? AND ip_v4=?", (id, ip))
res = c.fetchall()
print(res)
conn.close()