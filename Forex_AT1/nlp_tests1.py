import sqlite3
import spacy
import dateutil.parser
import matplotlib.pyplot as plt
from main_functions1 import *

from datetime import datetime  
from datetime import timedelta


conn = sqlite3.connect('example1.db')
c = conn.cursor()



def retrieveArticles():
	c.execute('''SELECT dateAndTime, title, description FROM googleNewsData ORDER BY dateTime(dateAndTime)''')
	newsTimeList = []
	lemmaArticleList = []
	data = c.fetchall()
	for i in range(len(data)):
		newsTimeList.append(data[i][0][:16] + '-06:00')

		newString = ""
		if data[i][1]:
			newString += data[i][1] + ' '
		if data[i][2]:
			newString += data[i][2]

		lemmaWordList = nltkLemmaList(newString)
		lemmaArticleList.append(lemmaWordList)

	return newsTimeList, lemmaArticleList


def makeLemmaArticleTable():
	c.execute('''CREATE TABLE IF NOT EXISTS lemmaArticleTable1 (dateAndTime TEXT, lemmaArticle TEXT, percentChange REAL)''')
	conn.commit()

	for i in range(len(lemmaArticleList)):
		dateAndTimeVal = newsTimeList[i]
		lemmaArticleVal = ' '.join(lemmaArticleList[i])

		curDateAndTime  = dateutil.parser.parse(dateAndTimeVal[:15] + '0-06:00') + timedelta(minutes=10)
		c.execute('''SELECT open FROM oandaEurusdData WHERE dateTime(dateAndTime)=dateTime(?)''',
			(curDateAndTime.isoformat(),))
		data = c.fetchall()
		if not data:
			continue
		curPrice = data[0][0]
		aftDateAndTime = curDateAndTime + timedelta(hours=2)
		c.execute('''SELECT open FROM oandaEurusdData WHERE dateTime(dateAndTime)=dateTime(?)''',
			(aftDateAndTime.isoformat(),))
		data = c.fetchall()
		if not data:
			continue
		aftPrice = data[0][0]
		pcVal = ((aftPrice - curPrice) / curPrice) * 100

		c.execute('''INSERT INTO lemmaArticleTable1 VALUES (?,?,?)''',
			(dateAndTimeVal, lemmaArticleVal, pcVal))
		conn.commit()




# newsTimeList, lemmaArticleList = retrieveArticles()
# makeLemmaArticleTable()
