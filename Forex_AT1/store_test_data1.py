import sqlite3
import dateutil.parser
from main_functions1 import *

from datetime import datetime  
from datetime import timedelta


conn = sqlite3.connect('example1.db')
c = conn.cursor()


def createTables():
	c.execute('''CREATE TABLE IF NOT EXISTS oandaEurusdData (dateAndTime TEXT, frequency TEXT, close REAL, high REAL, low REAL, open REAL,  volume INTEGER)''')
	conn.commit()

	c.execute('''CREATE TABLE IF NOT EXISTS googleNewsData (dateAndTime TEXT, q TEXT, title TEXT, description TEXT)''')
	conn.commit()

	c.execute('''CREATE TABLE IF NOT EXISTS intrinioData (dateAndTime TEXT, identifier TEXT, idValue REAL)''')
	conn.commit()


def storeOandaPriceData(startTimeVal, endTimeVal, instrumentVal, frequencyVal):
	data = retrieveOandaPrices(startTimeVal, endTimeVal, instrumentVal, frequencyVal)
	try:
		data = data['candles']
		for i in range(len(data)):
			dateAndTimeVal = data[i]['time'][:16] + 'Z'
			closeVal = float(data[i]['mid']['c'])
			highVal = float(data[i]['mid']['h'])
			lowVal = float(data[i]['mid']['l'])
			openVal = float(data[i]['mid']['o'])
			volumeVal = int(data[i]['volume'])

			c.execute('''INSERT INTO oandaEurusdData VALUES (?,?,?,?,?,?,?)''',
				(dateAndTimeVal, frequencyVal, closeVal, highVal, lowVal, openVal, volumeVal))
			conn.commit()
	except:
		print(data)

def storeGNData(startTimeVal, endTimeVal, qVal):
	data = retrieveGoogleNews(startTimeVal, endTimeVal, q=qVal)
	print("status: ", data['status'])
	print("totalResults: ", data['totalResults'])
	data = data['articles']
	for i in range(len(data)):
		dateAndTimeVal = data[i]['publishedAt']
		titleVal = data[i]['title']
		descriptionVal = data[i]['description']

		c.execute('''INSERT INTO googleNewsData VALUES (?,?,?,?)''',
			(dateAndTimeVal, qVal, titleVal, descriptionVal))
		conn.commit()

def storeIntrinioData(startTimeVal, endTimeVal):
	data1 = retrieveIntrinioData('$GDP', 'level', startTimeVal, endTimeVal, 'quarterly')
	if data1['result_count'] > 0:
		for i in range(len(data1['data'])):
			dateAndTimeVal = data1['data'][i]['date']
			identifierVal = data1['identifier']
			idValueVal = data1['data'][i]['value']

			c.execute('''INSERT INTO intrinioData VALUES (?,?,?)''',
				(dateAndTimeVal, identifierVal, idValueVal))
			conn.commit()

	data2 = retrieveIntrinioData('$PAYEMS', 'level', startTimeVal, endTimeVal, 'monthly')
	if data1['result_count'] > 0:
		for i in range(len(data2['data'])):
			dateAndTimeVal = data2['data'][i]['date']
			identifierVal = data2['identifier']
			idValueVal = data2['data'][i]['value']

			c.execute('''INSERT INTO intrinioData VALUES (?,?,?)''',
				(dateAndTimeVal, identifierVal, idValueVal))
			conn.commit()



def clearTable(table):
	c.execute('''DELETE FROM ''' +table)
	conn.commit()


def selectDuplicates(table, col):
	c.execute('''SELECT * FROM ''' +table+ ''' WHERE ''' +col+ ''' IN (
		 			SELECT ''' +col+ '''
		 			FROM ''' +table+ '''
		 			GROUP BY ''' +col+ '''
		 			HAVING count(*)>1 )
		 		AND ROWID NOT IN (
		 			SELECT ROWID
		 			FROM ''' +table+ '''
		 			GROUP BY ''' +col+ '''
		 			HAVING count(*)>1 ) ''')

	retRows = c.fetchall()
	for row in retRows:
		print(row)

def deleteDuplicates(table, col):
	c.execute('''DELETE FROM ''' +table+ ''' WHERE ''' +col+ ''' IN (
		 			SELECT ''' +col+ '''
		 			FROM ''' +table+ '''
		 			GROUP BY ''' +col+ '''
		 			HAVING count(*)>1 )
		 		AND ROWID NOT IN (
		 				SELECT ROWID
			 			FROM ''' +table+ '''
			 			GROUP BY ''' +col+ '''
			 			HAVING count(*)>1 ) ''')

	conn.commit()




def createDateList(startDate, endDate, daysSkip):
	startD = dateutil.parser.parse(startDate)
	endD = dateutil.parser.parse(endDate)

	delta = endD - startD
	dayCount = delta.days

	dateList = []
	for x in range(0, dayCount, daysSkip):
		newDate = endD - timedelta(days = x)
		dateList.append(newDate.isoformat())

	return dateList


def storeImportantGNData(startDate, endDate):
	dateList = createDateList(startDate, endDate, 5)
	print(dateList)

	# interest rate
	# federal reserve
	# federal funds rate
	# european central bank
	# minimum bid rate

	# employment
	# non farm
	# labor statistics

	# gross domestic product
	# us trade balance
	# us retail sales
	# us consumer price
	# us producer price index

	qList = [
			'federal funds rate',
			'minimum bid rate',
			'employment',
			'non farm',
			'labor statistics',
			'gross domestic product'
			]
	
	for i in range(len(dateList)):
		for q in qList:
			try:
				storeGNData(dateList[i], dateList[i+1], qVal=q)
			except IndexError:
				continue

	deleteDuplicates('''googleNewsData''', '''description''')


def storeMultipleOandaData(startDate, endDate):
	dateList = createDateList(startDate, endDate, 10)
	dateList.reverse()
	print(dateList)
	
	for i in range(len(dateList)):
		try:
			storeOandaPriceData(dateList[i], dateList[i+1], 'EUR_USD', 'M10')
		except IndexError:
			continue

	deleteDuplicates('''oandaEurusdData''', '''dateAndTime''')




# oandaEurusdData
# googleNewsData
# intrinioData
# lemmaArticleTable1

clearTable('''lemmaArticleTable1''')


# storeImportantGNData('2017-12-22', '2018-01-16')

# storeMultipleOandaData('2017-12-22T00:00:00-06:00', '2018-03-25T00:00:00-06:00')



# createTables()

# storeOandaPriceData('2017-12-19T00:00:00-06:00', '2017-12-20T00:00:00-06:00', 'EUR_USD', 'M15')

# storeGNData('2017-12-15T00:00:00-06:00', '2017-12-25T00:00:00-06:00', qVal='eurusd')

# deleteDuplicates('''googleNewsData''', '''description''')

# storeIntrinioData('2017-03-01', '2018-03-03')


#close connection
conn.close()