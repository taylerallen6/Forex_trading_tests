import sqlite3
import dateutil.parser
from main_functions1 import *

from datetime import datetime  
from datetime import timedelta


conn = sqlite3.connect('Forex_AT2.db')
c = conn.cursor()

######################################################################
######################################################################





def storeOandaPriceData(tableName, startTimeVal, endTimeVal, instrumentVal, frequencyVal):
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

			c.execute('''INSERT INTO ''' +tableName+ ''' VALUES (?,?,?,?,?,?,?)''',
				(dateAndTimeVal, frequencyVal, closeVal, highVal, lowVal, openVal, volumeVal))
			conn.commit()
	except:
		print(data)


def storeGNData(tableName, startTimeVal, endTimeVal, qVal):
	data = retrieveGoogleNews(startTimeVal, endTimeVal, q=qVal)
	print("status: ", data['status'])
	print("totalResults: ", data['totalResults'])
	data = data['articles']
	for i in range(len(data)):
		dateAndTimeVal = data[i]['publishedAt']
		titleVal = data[i]['title']
		descriptionVal = data[i]['description']

		c.execute('''INSERT INTO ''' +tableName+ ''' VALUES (?,?,?,?)''',
			(dateAndTimeVal, qVal, titleVal, descriptionVal))
		conn.commit()


def clearTable(table):
	c.execute('''DELETE FROM ''' +table)
	conn.commit()


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



########################################################################
########################################################################



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


def storeMultipleOandaData(tableName, startDate, endDate, daysSkip, instrumentVal, frequencyVal):
	c.execute('''CREATE TABLE IF NOT EXISTS ''' +tableName+ ''' (dateAndTime TEXT, frequency TEXT, close REAL, high REAL, low REAL, open REAL,  volume INTEGER)''')
	conn.commit()

	dateList = createDateList(startDate, endDate, daysSkip)
	dateList.reverse()
	print(dateList)
	
	for i in range(len(dateList)):
		try:
			storeOandaPriceData(tableName, dateList[i], dateList[i+1], instrumentVal, frequencyVal)
			print(i, len(dateList))
		except IndexError:
			continue

	deleteDuplicates(tableName, '''dateAndTime''')


def storeImportantGNData(tableName, startDate, endDate, daysSkip):
	c.execute('''CREATE TABLE IF NOT EXISTS ''' +tableName+ ''' (dateAndTime TEXT, q TEXT, title TEXT, description TEXT)''')
	conn.commit()

	dateList = createDateList(startDate, endDate, daysSkip)
	dateList.reverse()
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
				storeGNData(tableName, dateList[i], dateList[i+1], qVal=q)
			except IndexError:
				continue

	deleteDuplicates(tableName, '''description''')



######################################################################
######################################################################



# OandaDataTable1
# GNDataTable1


# clearTable('''OandaDataTable1''')
# clearTable('''GNDataTable1''')
storeMultipleOandaData('''OandaDataTableD1_5years''', '2013-07-30T00:00:00-00:00', '2018-07-30T00:00:00-00:00', 10, 'EUR_USD', 'D')
# storeImportantGNData('''GNDataTable1''', '2018-01-22', '2018-01-24', 1)



######################################################################
######################################################################

conn.close()