import sqlite3


with open('test_data.sql', 'r') as sql_file:
    sql_script = sql_file.read()


con = sqlite3.connect("database.db")
cur = con.cursor()

cur.executescript(sql_script)
con.commit()
