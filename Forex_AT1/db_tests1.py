import sqlite3

conn = sqlite3.connect('example1.db')
c = conn.cursor()

# create table
c.execute('''CREATE TABLE IF NOT EXISTS testTable1 (closePrice REAL, dateAndTime TEXT) ''')

# insert a row
c.execute('''INSERT INTO testTable1 VALUES (2.139841, '2018-05-10')''')

#save changes
conn.commit()

#close connection
conn.close()