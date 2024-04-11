import requests
import json
import sqlite3
import dateutil.parser
from pprint import pprint

from datetime import datetime
from datetime import timedelta

import pandas as pd
import sqlalchemy as db


# sqlite_file = '10_min_forex.db'
sqlite_file = '10_min_major_pairs.db'
engine = db.create_engine('sqlite:///'+ sqlite_file)
conn = engine.connect()

#######################################################################################
#######################################################################################



def retrieve_oanda_prices(start_time, end_time, instrument, frequency):
	url = 'https://api-fxtrade.oanda.com/v3/instruments/{instrument}/candles'.format(instrument=instrument)
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ebf9324a166c0e141bf49fb0f43c4b96-1ea671e8b910b9e756b8bd5fb1dd1196',
	}
	params = (
		# ('count', '5000'),

		('from', start_time),
		('to', end_time),

		('price', 'M'),
		('granularity', frequency)
	)
	r = requests.get(url, headers=headers, params=params)

	return r.json()

# data = retrieve_oanda_prices('2017-01-01T00:00:00-00:00', '2017-02-01T00:00:00-00:00', 'EUR_USD', 'M10')
# pprint(data)


def store_oanda_price_data(table_name, start_time_val, end_time_val, instrument_val, frequency_val):
	data = retrieve_oanda_prices(start_time_val, end_time_val, instrument_val, frequency_val)
	try:
		data = data['candles']
		df = pd.DataFrame()
		for i in range(len(data)):
			temp = {}
			temp['date_and_time'] = [data[i]['time'][:16] + 'Z']
			temp['close'] = [float(data[i]['mid']['c'])]
			temp['high'] = [float(data[i]['mid']['h'])]
			temp['low'] = [float(data[i]['mid']['l'])]
			temp['open'] = [float(data[i]['mid']['o'])]
			temp['volume'] = [int(data[i]['volume'])]

			temp = pd.DataFrame(temp)
			df = df.append(temp)

		df.to_sql(table_name, conn, index=False, if_exists="append")

	except Exception as e:
		print('FOUND EXCEPTION')
		print(str(e))
		# pprint(data)

	return

def store_oanda_price_data2(table_name, start_time_val, end_time_val, instrument_val, frequency_val):
	data = retrieve_oanda_prices(start_time_val, end_time_val, instrument_val, frequency_val)
	try:
		data = data['candles']
		df = pd.DataFrame()
		for i in range(len(data)):
			temp = {}
			temp[instrument_val + 'datetime'] = [data[i]['time'][:16] + 'Z']
			temp[instrument_val + 'close'] = [float(data[i]['mid']['c'])]
			temp[instrument_val + 'high'] = [float(data[i]['mid']['h'])]
			temp[instrument_val + 'low'] = [float(data[i]['mid']['l'])]
			temp[instrument_val + 'open'] = [float(data[i]['mid']['o'])]
			temp[instrument_val + 'volume'] = [int(data[i]['volume'])]

			temp = pd.DataFrame(temp)
			df = df.append(temp)

		df.to_sql(table_name, conn, index=False, if_exists="append")

	except Exception as e:
		print('FOUND EXCEPTION')
		print(str(e))
		# pprint(data)

	return

# store_oanda_price_data('prices1', '2019-06-03T00:00:00-00:00', '2019-06-05T00:00:00-00:00', 'EUR_USD', 'M1')


def delete_duplicates(table, col):
	sql = '''DELETE FROM {table} WHERE {col} IN (
				SELECT {col} FROM {table} GROUP BY {col} HAVING count(*)>1 ) 
			AND ROWID NOT IN (
				SELECT ROWID FROM {table} GROUP BY {col} HAVING count(*)>1 )'''.format(
			table=table, col=col)

	conn.execute(sql)

	return

# delete_duplicates('prices1', 'date_and_time')


def create_date_list(start_date, end_date, days_skip):
	start_d = dateutil.parser.parse(start_date)
	end_d = dateutil.parser.parse(end_date)

	delta = end_d - start_d
	days_count = delta.days
	# seconds_skip = days_skip * 60 * 60 * 24

	date_list = []
	for x in range(0, days_count, days_skip):
		new_date = end_d - timedelta(days=x)
		date_list.append(new_date.isoformat())

	return date_list

# date_list = create_date_list('2019-06-01T00:00:00-00:00', '2019-06-12T0:00:00-00:00', 2)
# print(date_list)

def create_table(table_name):
	sql = '''CREATE TABLE IF NOT EXISTS {}(
				datetime TEXT NOT NULL,
				close REAL NOT NULL,
				high REAL NOT NULL,
				low REAL NOT NULL,
				open REAL NOT NULL,
				volume INT NOT NULL
			)'''.format(table_name)

	conn.execute(sql)

	return

def delete_table(table_name):
	sql = '''DROP TABLE IF EXISTS {}'''.format(table_name)
	conn.execute(sql)

	return

def store_daily_oanda_prices(table_name, start_date, end_date, instrument_val):
	delete_table(table_name)
	create_table(table_name)
	store_oanda_price_data(table_name, start_date, end_date, instrument_val, 'D')

	return

def store_multiple_oanda_prices(table_name, start_date, end_date, days_skip, instrument_val, frequency_val):
	date_list = create_date_list(start_date, end_date, days_skip)
	date_list.reverse()
	print(date_list)

	create_table(table_name)

	for i in range(len(date_list)):
		try:
			store_oanda_price_data(table_name, date_list[i], date_list[i+1], instrument_val, frequency_val)
			print(i, len(date_list))
		except IndexError:
			continue

	delete_duplicates(table_name, 'date_and_time')

	return

def store_multiple_oanda_prices2(table_name, start_date, end_date, days_skip, instrument_list, frequency_val):
	date_list = create_date_list(start_date, end_date, days_skip)
	date_list.reverse()
	print(date_list)

	create_table(table_name)

	for instrument_val in instrument_list:
		for i in range(len(date_list)):
			try:
				store_oanda_price_data2(table_name, date_list[i], date_list[i+1], instrument_val, frequency_val)
				print(i, len(date_list))
			except IndexError:
				continue

	delete_duplicates(table_name, 'date_and_time')

	return

# EUR/USD eur_usd1
# USD/JPY usd_jpy1
# GBP/USD gbp_usd1
# AUD/USD aud_usd1
# USD/CAD usd_cad1
# USD/CNY usd_cny1 X
# USD/CHF
# EUR/GBP
# USD/MXN
# USD/SGD
# https://www.ig.com/en/news-and-trade-ideas/forex-news/top-10-most-traded-currency-pairs-190213

# store_multiple_oanda_prices('eur_usd1', '2016-01-01T00:00:00-00:00', '2020-06-01T0:00:00-00:00', 25, 'EUR_USD', 'M10')
# store_daily_oanda_prices('eur_usd1', '2016-06-01T00:00:00-00:00', '2020-06-01T00:00:00-00:00', 'EUR_USD')

instrument_list = [
	'AUD_JPY',
	'AUD_USD',
	'EUR_AUD',
	'EUR_CHF',
	'EUR_GBP',
	'EUR_JPY',
	'EUR_USD',
	'GBP_CHF',
	'GBP_JPY',
	'GBP_USD',
	'NZD_USD',
	'USD_CAD',
	'USD_CHF',
	'USD_JPY'
]
store_multiple_oanda_prices2('table1', '2020-01-01T00:00:00-00:00', '2020-06-01T0:00:00-00:00', 25, instrument_list, 'M10')

conn.close()