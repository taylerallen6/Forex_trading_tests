import sqlite3
import spacy
import dateutil.parser
import matplotlib.pyplot as plt
import statistics
from main_functions1 import *


conn = sqlite3.connect('example1.db')
c = conn.cursor()





c.execute('''SELECT * FROM lemmaArticleTable1 ORDER BY dateTime(dateAndTime)''')
priceTimeList = []
lemmaArticleList = []
pcList = []
data = c.fetchall()
for i in range(len(data)):
	priceTimeList.append(dateutil.parser.parse(data[i][0]))

	lemmaArticle = data[i][1].split()
	lemmaArticleList.append(lemmaArticle)

	percentChange = data[i][2]
	pcList.append(percentChange)



listLength = len(lemmaArticleList)
adjustedListLength = listLength-1000

totalPC = 0
for i in range(adjustedListLength, listLength):

	pcValList = []
	for ii in range(i):

		simPercent = ArticleSimCheck(lemmaArticleList[i], lemmaArticleList[ii])
		# print(simPercent)
		if simPercent > 50:
			pcValList.append(pcList[ii])
			# print('ABOVE 50 PERCENT')

	if len(pcValList) > 4:
		pcValList.sort()

		averagePcVal = sum(pcValList)/len(pcValList)
		medPcVal = statistics.median(pcValList)
		estimatedPcVal = (averagePcVal + medPcVal)/2

		# mid = int(len(pcValList) / 2)
		# if (len(pcValList) % 2 == 0):
		# 	lowerQ = statistics.median(pcValList[:mid])
		# 	upperQ = statistics.median(pcValList[mid:])
		# else:
		# 	lowerQ = statistics.median(pcValList[:mid])
		# 	upperQ = statistics.median(pcValList[mid+1:])

		# if lowerQ/abs(lowerQ) == upperQ/abs(upperQ):

		
		# print(medPcVal)
		# print(estimatedPcVal)
		if medPcVal != 0 and estimatedPcVal != 0:
			if medPcVal/abs(medPcVal) == estimatedPcVal/abs(estimatedPcVal):

				if abs(estimatedPcVal) > .01:

					absPcValList = []
					for ii in range(len(pcValList)):
						absPcValList.append(abs(pcValList[ii]))
					pcValListRange = max(pcValList) - min(pcValList)
					convictionVal = 1
					if pcValListRange != 0:
						convictionVal = ((max(absPcValList)-(pcValListRange/2)) / (pcValListRange/2)) * 100

					if convictionVal > 70:
						print()
						print(pcValList)
						print("ESTIMATED PC: ", estimatedPcVal)
						print("REAL PC: ", pcList[i])
						print("CONVICTION VAL: ", convictionVal)

						if estimatedPcVal > 0 and pcList[i] > 0 or estimatedPcVal < 0 and pcList[i] < 0:
							print("Right!!!!!!!!!!!!!!")
							totalPC += abs(pcList[i])
						else:
							print("Wrong!!!!!!!!!!!!!!!!!!")
							totalPC -= abs(pcList[i])
						totalPC -= .00

						print()
						# print("lowerQ: ", lowerQ)
						# print("upperQ: ", upperQ)
						# print()
						print(priceTimeList[i])
						print("TOTALPC: ", totalPC)
						# print()

print()
print("TOTALPC: ", totalPC)








# plt.plot(priceTimeList, openPriceList, 'bo-',   newsTimeList, [min(openPriceList)]*len(newsTimeList), 'ro')
# plt.plot(priceTimeList, pcOpenList, 'bo',   newsTimeList, [0]*len(newsTimeList), 'ro')
# plt.plot(intrinioTimeList, pcNfpList, 'ro')



# plt.plot(priceTimeList, pcList, 'ro')

# plt.xticks(rotation=-90)
# plt.tight_layout()
# plt.grid(True)
# plt.show()

# close connection
conn.close()