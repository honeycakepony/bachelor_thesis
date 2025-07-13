import sqlite3

# -------------------------------------------------------------------
# No need to run this if 'pdp_source_1.db' is working on your machine
# -------------------------------------------------------------------

### setup
conn = sqlite3.connect('pdp_source_1.db')
c = conn.cursor()
c.execute('''CREATE TABLE subjects
             (
                 id           text,
                 type         text,
                 fingerprint  text,
                 device_id    text,
                 user_session text
             )''')

### filling database
c.execute("INSERT INTO subjects VALUES ('ethan@mission−thesis.org', 'user', '30cd5227e750fe8848fc32fd4683b8d66e654567c708445be76bc8fe34f2dc74', '8:65:cc:18:8c:0c', 'aHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f')")
c.execute("INSERT INTO subjects VALUES ('luther@mission−thesis.org', 'user', '7514118a4a9aa4a0998d4e14efbfd73550bfcb08e313bb87e7f4bdd8b22a2ef4', '8:65:cc:18:8c:0c', 'bHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f')")
c.execute("INSERT INTO subjects VALUES ('neely@mission−thesis.org', 'user', '8ba3777ed04eb2e09368b29d6154beb54c045e8d1474d1b91e240fe0e6365cad','8:65:cc:18:8c:0c', 'gHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f')")
c.execute("INSERT INTO subjects VALUES ('gabriel@mission−thesis.org', 'user', 'fef2e6094100944eb27f5aa88f3fe110ce2a7066d0d68256c1ec621776339349', '2:42:aa:e8:8d:0c', 'hHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f')")

c.execute("INSERT INTO subjects VALUES ('account3@mission−thesis.org', 'user', '38eda86f21d3c8c316d08b376ec437051cf3d7146d79c7301bd6d63b4fc8b0af', '4:41:bb:ee:8f:0c', '66d8c683f483cc9c0e7335b25ec25cd490da5111123a87b4')")

c.execute("INSERT INTO subjects VALUES ('c-3po@mission−thesis.org', 'machine', '7b0a5a3d1be219d969dbab402e034e4460d4c96828c9b2752079f8744ccd4a65', '8:65:cc:18:8c:0c', 'iHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f')")
c.execute("INSERT INTO subjects VALUES ('r2-d2@mission−thesis.org', 'machine', 'b21bcc91a557365030b22cb0de2d46e366500a567da790bb8de9648992417f25', '8:65:cc:18:8c:0c', 'jHQWx3VGAmhlsUDSxAWkuAmWgSDR4FW5dwCtkW2Glt9HQU8f')")


### final steps
conn.commit()
conn.close()
