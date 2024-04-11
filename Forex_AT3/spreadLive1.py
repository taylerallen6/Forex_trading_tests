import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sqlite3

import requests
import json
from pprint import pprint



spreadVal = .0002
profitVal = .0003
moveVal = spreadVal + profitVal


def retrieveOandaPrices(count, instrument, frequency):
	urlBegin = 'https://api-fxtrade.oanda.com/v3/instruments/'
	urlEnd = '/candles'
	url1 = urlBegin + instrument + urlEnd
	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': 'Bearer 2ea6e37355458482a2bbbf02278401aa-5dd31b361fd07b7db2b4624de48396a7',
	}
	params = (
		('count', count),
		('price', 'AB'),
		('granularity', frequency)
	)
	r = requests.get(url1, headers=headers, params=params)
	return r.json()

def retrieveCurrentOandaPrices(instrument):
	urlBegin = 'https://api-fxtrade.oanda.com/v3/accounts/'
	accountVal = '001-001-1584675-001'
	urlEnd = '/pricing'
	url1 = urlBegin + accountVal + urlEnd
	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': 'Bearer 2ea6e37355458482a2bbbf02278401aa-5dd31b361fd07b7db2b4624de48396a7',
	}
	params = (
		('instruments', instrument),
	)
	r = requests.get(url1, headers=headers, params=params)
	return r.json()


oanda_data = retrieveOandaPrices('3', 'EUR_USD', 'D')
pprint(oanda_data['candles'][0]['ask'])

# oanda_current_data = retrieveCurrentOandaPrices('EUR_USD')
# pprint(oanda_current_data['prices'][0]['tradeable'])
# pprint(oanda_data)