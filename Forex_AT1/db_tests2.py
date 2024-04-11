import sqlite3

# create connection
conn = sqlite3.connect('example1.db')
c = conn.cursor()



# create table
def createTable():
	c.execute('''CREATE TABLE IF NOT EXISTS testTable1 (closePrice REAL, dateAndTime TEXT)''')
	#save changes
	conn.commit()

# delete table
def dropTable():
	c.execute('''DROP TABLE testTable1''')
	conn.commit()



# insert a row
def insertRow(closePriceVal, dateAndTimeVal):
	c.execute('''INSERT INTO testTable1 VALUES (?, ?)''',
		(closePriceVal, dateAndTimeVal))
	#save changes
	conn.commit()

# make changes to specified rows
def updateRows(closePriceVal, dateAndTimeVal):
	c.execute('''UPDATE testTable1 SET closePrice=? WHERE datetime(dateAndTime) = datetime(?)''',
		(closePriceVal, dateAndTimeVal))
	#save changes
	conn.commit()

# delete specified rows from table
def deleteFromTable(dateAndTimeVal):
	c.execute('''DELETE FROM testTable1 WHERE datetime(dateAndTime) = datetime(?)''',
		(dateAndTimeVal,))
	#save changes
	conn.commit()

# delete all rows from table
def deleteAllInTable():
	c.execute('''DELETE FROM testTable1''')
	#save changes
	conn.commit()



# retrieve list of table names
def retrieveTableNames():
	c.execute('''SELECT name FROM sqlite_master WHERE type = "table"''')
	tables = c.fetchall()
	for table in tables:
		print(table[0])

# retrieve all rows
def retrieveAll():
	c.execute('''SELECT * FROM testTable1''',)
	retRows = c.fetchall()
	for row in retRows:
		print(row)

# retrieve row by ROWID
def retrieveByROWID(rowIdVal):
	c.execute('''SELECT * FROM testTable1 WHERE ROWID=?''',
		(rowIdVal,))
	retRows = c.fetchall()
	for row in retRows:
		print(row)

# retrieve row(s) by datetime
def retrieveByDateTime(dateAndTimeVal):
	c.execute('''SELECT * FROM testTable1 WHERE datetime(dateAndTime) = datetime(?)''',
		(dateAndTimeVal,))
	retRows = c.fetchall()
	for row in retRows:
		print(row)











# close connection
conn.close()