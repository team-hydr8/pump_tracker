import sqlite3
import os

DB_FILE = "database.db"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Old database removed.")

con = sqlite3.connect(DB_FILE)
cur = con.cursor()

with open('ddl.sql', 'r') as sql_file:
    sql_script = sql_file.read()
cur.executescript(sql_script)
print("Database schema created successfully.")

with open('test_data.sql', 'r') as sql_file:
    sql_script = sql_file.read()
cur.executescript(sql_script)
print("Test data inserted successfully.")

con.commit()
con.close()