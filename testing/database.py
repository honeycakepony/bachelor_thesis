import sqlite3

### setup
conn = sqlite3.connect('pdp_source_1.db')
c = conn.cursor()
# c.execute('''CREATE TABLE users
#              (
#                  id          text PRIMARY KEY,
#                  type        text,
#                  fingerprint text
#              )''')

### filling database
# c.execute("INSERT INTO users VALUES ('ethan@basic−connect.org', 'user', 'dfd0fd7af55ab8de9aa656c3706dbc1d85713480')")
c.execute("SELECT * FROM users WHERE fingerprint='dfd0fd7af55ab8de9aa656c3706dbc1d85713480'")
c.fetchall() # returns Ethan
c.execute("SELECT * FROM users WHERE fingerprint='afd0fd7af55ab8de9aa656c3706dbc1d85711480'")
c.fetchall() # returns nothing

### final steps
conn.commit()
conn.close()
