import sqlite3
import spacy
import dateutil.parser
import matplotlib.pyplot as plt
import statistics
from main_functions1 import *


conn = sqlite3.connect('example1.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS FxQtable1 (lemmaArticle TEXT, articleWeights TEXT, articlesActionVals TEXT, tradeActionVals TEXT)''')
conn.commit()

#
#	articleWeights = time, 
#	articleActionVals = 1 article, 2 articles, 3 articles, 4 articles, 5 articles
#	tradeActionVals = 20 minutes, 30 min, 40 min, 50 min, 60 min
#



c.execute('''SELECT * FROM lemmaArticleTable1 ORDER BY dateTime(dateAndTime)''')
priceTimeList = []
lemmaArticleList = []
mainData = c.fetchall()
for i in range(len(mainData)):
	priceTimeList.append(dateutil.parser.parse(mainData[i][0]))

	lemmaArticle = mainData[i][1].split()
	lemmaArticleList.append(lemmaArticle)





listLength = len(lemmaArticleList)
adjustedListLength = listLength-1000


totalPC = 0
for i in range(adjustedListLength, listLength):

	c.execute('''INSERT INTO FxQtable1 VALUES (?, ?, ?, ?)''',
		(lemmaArticleList[i], "0", "0,0,0,0,0", "0,0,0,0,0",))

	c.execute('''SELECT lemmaArticle FROM FxQtable1''')
	data1 = c.fetchall()

	memoryArticleList = []
	for ii in range(len(data1)):
		priceTimeList.append(dateutil.parser.parse(data1[ii][0]))

		memoryArticle = data1[ii][1].split()
		memoryArticleList.append(memoryArticle)

	retrievedAcrticles = []
	for ii in range(len(memoryArticleList)):
		simPercent = ArticleSimCheck(lemmaArticleList[i], memoryArticleList[ii])
		if simPercent > 75.0:
			retrievedAcrticles.append(memoryArticleList[ii])

	articleActionVals = [0,0,0,0,0]
	tradeActionVals = [0,0,0,0,0]
	for ii in range(len(retrievedAcrticles)):
		retArtString = (' '.join(str(x) for x in retrievedAcrticles[ii]))
		c.execute('''SELECT * FROM FxQtable1 WHERE lemmaArticle=?''',
			(retArtString,))
		data2 = c.fetchall()


# close connection
conn.close()