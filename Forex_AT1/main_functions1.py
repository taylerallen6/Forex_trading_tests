import requests
import json
import sqlite3
import spacy

import nltk
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords





def retrieveOandaPrices(startTime, endTime, instrument, frequency):
	urlBegin = 'https://api-fxtrade.oanda.com/v3/instruments/'
	urlEnd = '/candles'
	url1 = urlBegin + instrument + urlEnd
	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': 'Bearer 2ea6e37355458482a2bbbf02278401aa-5dd31b361fd07b7db2b4624de48396a7',
	}
	params = (
		# ('count', '5'),

		('from', startTime),
		('to', endTime),

		('price', 'M'),
		('granularity', frequency)
	)
	r = requests.get(url1, headers=headers, params=params)
	return r.json()


def retrieveGoogleNews(startTime, endTime, q):
	url1 = 'https://newsapi.org/v2/everything'
	params = (
		('from', startTime),
		('to', endTime),
		('language', 'en'),
		('sortBy', 'publishedAt'),
		('pageSize', '100'),
	    ('apiKey', '190074c1641c41d0afd1da3745410823'),

	    ('q', q),
	    # ('sources', 'cnbc'),
	)
	r = requests.get(url1, params=params)
	return r.json()


def retrieveIntrinioData(identifier, itemType, startTime, endTime, frequency):
	url1 = 'https://api.intrinio.com/historical_data'
	params = (
		('identifier', identifier),
		('item', itemType),

		('start_date', startTime),
		('end_date', endTime),

		('frequency', frequency),
	)
	auth = ('671d9ac2bc1b1204c5fb56e8b61f3936', '6430d60d86565fddc1d05b99b1644cc5')
	r = requests.get(url1, params=params, auth=auth)
	return r.json()


def retrieveTwitterData():
	url1 = 'https://api.twitter.com/1.1/search/tweets.json'
	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': 'Bearer 2ea6e37355458482a2bbbf02278401aa-5dd31b361fd07b7db2b4624de48396a7',
	}
	params = (
		# ('count', '5'),

		('from', startTime),
		('to', endTime),

		('price', 'M'),
		('granularity', frequency)
	)
	r = requests.get(url1, headers=headers, params=params)
	return r.json()



def makeLemmaWordList(inpString):
	nlp = spacy.load("en")
	spacyDoc = nlp(inpString.lower())

	wordList = []
	for token in spacyDoc:
		if not token.is_stop and not token.is_punct:
			wordList.append(token.lemma_)

	return wordList



lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
def nltkLemmaList(stringVal):
	tokenizer = RegexpTokenizer(r'\w+')
	wordList = tokenizer.tokenize(stringVal.lower())
	newWordList = []
	for word in wordList:
		if word not in stop_words:
			newWordList.append(word)

	lemmaWordList = []
	for word, pos in pos_tag(newWordList):
		if pos[0].lower() in ['a','n','v']:
			lemmaWordList.append(lemmatizer.lemmatize(word, pos=pos[0].lower()))
		else:
			lemmaWordList.append(lemmatizer.lemmatize(word))

	return lemmaWordList






def ArticleSimCheck(list1, list2):
	simPercent = 100.0
	if list1 != list2:

		simVal = 0
		for i in range(len(list1)):
			for ii in range(len(list2)):
				if list1[i] == list2[ii]:
					sim = (len(list1) - abs(ii-i))
					if sim < 0:
						sim = 0
					simVal += sim
					# print("SimVal: ",simVal, "--------", list1[i], "--------")

		simPercent = (simVal / (len(list1) * len(list2))) * 100

	return simPercent