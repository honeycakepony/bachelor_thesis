import sqlite3

# Note:
#       IPv4 addresses found using https://whatismyipaddress.com/, last access 6 June 2025
#

### setup
conn = sqlite3.connect('pdp_source_1.db')
c = conn.cursor()
c.execute('''CREATE TABLE users
             (
                 id          text,
                 type        text,
                 fingerprint text,
                 ip_v4       text
             )''')

### filling database
c.execute("INSERT INTO users VALUES ('ethan@mission−thesis.org', 'user', '30cd5227e750fe8848fc32fd4683b8d66e654567c708445be76bc8fe34f2dc74', '217.233.97.120')")
c.execute("INSERT INTO users VALUES ('luther@mission−thesis.org', 'user', '7514118a4a9aa4a0998d4e14efbfd73550bfcb08e313bb87e7f4bdd8b22a2ef4', '84.181.56.232')")
c.execute("INSERT INTO users VALUES ('benji@mission−thesis.org', 'user', '7fe4b905551afccadc607aef597cfac76c574140ee669d3efb820a52a4608ac0', '78.54.4.105')")
c.execute("INSERT INTO users VALUES ('eugene@mission−thesis.org', 'user', '33cebc860c200f6dc82d457fbfd424891c203262baca32c65c520f3887631c75', '79.208.218.53')")
c.execute("INSERT INTO users VALUES ('grace@mission−thesis.org', 'user', '4a0088e70647d774b4b849ba4e0aa7c5cc6d1a59d369f66b1b1c001b8bf70e74', '194.228.235.234')")
c.execute("INSERT INTO users VALUES ('paris@mission−thesis.org', 'user', 'c4f42a7021bee97976d6a98366f7f3d8f8a9f8dda3adfffd805b9e0e1d42033f', '91.160.93.4')")
c.execute("INSERT INTO users VALUES ('neely@mission−thesis.org', 'user', '8ba3777ed04eb2e09368b29d6154beb54c045e8d1474d1b91e240fe0e6365cad', '196.247.180.132')")

# c.execute("SELECT * FROM users WHERE id='ethan@basic−connect.org'")
# c.fetchall() # returns Ethan
# c.execute("SELECT * FROM users WHERE fingerprint='dfd0fd7af55ab8de9aa656c3706dbc1d85713480'")
# c.fetchall() # returns Ethan
# c.execute("SELECT * FROM users WHERE fingerprint='afd0fd7af55ab8de9aa656c3706dbc1d85711480'")
# c.fetchall() # returns nothing

### final steps
conn.commit()
conn.close()
