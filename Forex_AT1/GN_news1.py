import requests
import json
import dateutil.parser
from main_functions1 import *

import spacy




nlp = spacy.load("en")

data = retrieveGoogleNews('2018-03-01T00:00:00-06:00', '2018-03-02T00:00:00-06:00', q='non farm payrolls')
formattedData = json.dumps(data, indent=3, sort_keys=True)
print(formattedData)


# totalList = []
# newsTimeList = []

# for article in data['articles']:
# 	newString = ""
# 	if article['title']:
# 		newString += article['title'] + ' '
# 	if article['description']:
# 		newString += article['description']

# 	time = article['publishedAt'][:16] + '-06:00'

# 	spacyDoc = nlp(newString.lower())

# 	wordList = []
# 	for token in spacyDoc:
# 		if not token.is_stop:
# 			wordList.append(token.lemma_)

# 	totalList.append(wordList)
# 	newsTimeList.append(dateutil.parser.parse(time))

# 	# print("PUBLISHED AT:  ", article['publishedAt'])
# 	# print("TITLE:  ", article['title'])
# 	# print("DESCRIPTION:  ", article['description'])
# 	# print("SOURCE:  ", article['source'])
# 	# print()

# print(len(data['articles']))

	# print(wordList)
	# print()
	# print()

	