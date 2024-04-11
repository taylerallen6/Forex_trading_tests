import requests
import json
import sqlite3
import dateutil.parser

from datetime import datetime  
from datetime import timedelta



conn = sqlite3.connect('Forex_AT2.db')
c = conn.cursor()

######################################################################
######################################################################



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



######################################################################
######################################################################

conn.close()