import requests
import json
import sqlite3
import dateutil.parser
from pprint import pprint

from datetime import datetime
from datetime import timedelta

import pandas as pd


def retrieve_oanda_data(start_time, end_time, instrument, frequency):
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

# data = retrieve_oanda_data('2010-06-1T0:00:00-00:00', '2020-06-01T0:00:00-00:00', 'NZD_USD', 'D')
# pprint(data)


def store_data(df, instrument_val, data):
	data = data['candles']
	for i in range(len(data)):
		temp = {}
		temp['datetime'] = [data[i]['time'][:16] + 'Z']
		temp[instrument_val + '-close'] = [float(data[i]['mid']['c'])]
		temp[instrument_val + '-high'] = [float(data[i]['mid']['h'])]
		temp[instrument_val + '-low'] = [float(data[i]['mid']['l'])]
		temp[instrument_val + '-open'] = [float(data[i]['mid']['o'])]
		temp[instrument_val + '-volume'] = [int(data[i]['volume'])]

		temp = pd.DataFrame(temp)
		df = df.append(temp)

	return df


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


def store_multiple_oanda_prices(csv_file, start_date, end_date, days_skip, instrument_list, frequency_val):
	date_list = create_date_list(start_date, end_date, days_skip)
	date_list.reverse()
	print(date_list)

	df_list = []

	for instrument_val in instrument_list:
		df_temp = pd.DataFrame()

		for i in range(len(date_list)):
			try:
				data = retrieve_oanda_data(date_list[i], date_list[i+1], instrument_val, frequency_val)
				df_temp = store_data(df_temp, instrument_val, data)
				df_temp.drop_duplicates()

				print("instrument {0}: {1} of {2}".format(instrument_val, i, len(date_list)))

			except IndexError:
				continue

		df_temp = df_temp.set_index('datetime')
		df_list.append(df_temp)
		print()

	df = pd.concat(df_list, axis=1, sort=False)
		
	print(df)
	df.to_csv(csv_file) 

	return


def store_multiple_daily_oanda_prices(csv_file, start_date, end_date, days_skip, instrument_list, frequency_val):
	df_list = []

	for instrument_val in instrument_list:
		print(instrument_val)
		df_temp = pd.DataFrame()

		try:
			data = retrieve_oanda_data(start_date, end_date, instrument_val, frequency_val)
			df_temp = store_data(df_temp, instrument_val, data)
			df_temp.drop_duplicates()

		except IndexError:
			continue

		df_temp = df_temp.set_index('datetime')
		df_list.append(df_temp)

	df = pd.concat(df_list, axis=1, sort=False)
		
	print(df)
	df.to_csv(csv_file) 

	return


def adjust_data(csv_file, new_csv_file, instrument_list):
	df = pd.read_csv(csv_file)
	# df = df.dropna()

	candle_values = ['open','high','low','close']

	def adjust_jpy(instr, candle_val):
		return df[instr+ '-' + candle_val] / df['USD_JPY-' + candle_val]
	def adjust_aud(instr, candle_val):
		return df[instr+ '-' + candle_val] * df['AUD_USD-' + candle_val]
	def adjust_chf(instr, candle_val):
		return df[instr+ '-' + candle_val] / df['USD_CHF-' + candle_val]
	def adjust_gbp(instr, candle_val):
		return df[instr+ '-' + candle_val] * df['GBP_USD-' + candle_val]
	def adjust_cad(instr, candle_val):
		return df[instr+ '-' + candle_val] / df['USD_CAD-' + candle_val]
	
	for candle_val in candle_values:
		print(candle_val)

		df['AUD_JPY-adjusted-' + candle_val] = adjust_jpy('AUD_JPY', candle_val)
		df['AUD_USD-adjusted-' + candle_val] = df['AUD_USD-' + candle_val]
		df['EUR_AUD-adjusted-' + candle_val] = adjust_aud('EUR_AUD', candle_val)
		df['EUR_CHF-adjusted-' + candle_val] = adjust_chf('EUR_CHF', candle_val)
		df['EUR_GBP-adjusted-' + candle_val] = adjust_gbp('EUR_GBP', candle_val)
		df['EUR_JPY-adjusted-' + candle_val] = adjust_jpy('EUR_JPY', candle_val)
		df['EUR_USD-adjusted-' + candle_val] = df['EUR_USD-' + candle_val]
		df['GBP_CHF-adjusted-' + candle_val] = adjust_chf('GBP_CHF', candle_val)
		df['GBP_JPY-adjusted-' + candle_val] = adjust_jpy('GBP_JPY', candle_val)
		df['GBP_USD-adjusted-' + candle_val] = df['GBP_USD-' + candle_val]
		df['NZD_USD-adjusted-' + candle_val] = df['NZD_USD-' + candle_val]
		df['USD_CAD-adjusted-' + candle_val] = adjust_jpy('USD_CAD', candle_val)
		df['USD_CHF-adjusted-' + candle_val] = adjust_jpy('USD_CHF', candle_val)
		df['USD_JPY-adjusted-' + candle_val] = adjust_jpy('USD_JPY', candle_val)
	
	df.to_csv(new_csv_file, index=False)

	return

def fix_index(csv_file):
	df = pd.read_csv(csv_file)
	print(df.columns)
	df = df.rename(columns={'Unnamed: 0': 'datetime'})
	print(df.columns)
	df.to_csv(csv_file, index=False)

	return

def simplify(csv_file, new_csv_file, instrument_list):
	df = pd.read_csv(csv_file)
	print(df.columns)

	df2 = pd.DataFrame()

	df2['datetime'] = df['Unnamed: 0']

	for instr in instrument_list:
		df2[instr + '-open'] = df[instr + '-open']
		df2[instr + '-high'] = df[instr + '-high']
		df2[instr + '-low'] = df[instr + '-low']
		df2[instr + '-close'] = df[instr + '-close']
		df2[instr + '-volume'] = df[instr + '-volume']

		# df2[instr + '-adjusted-open'] = df[instr + '-adjusted-open']
		# df2[instr + '-adjusted-high'] = df[instr + '-adjusted-high']
		# df2[instr + '-adjusted-low'] = df[instr + '-adjusted-low']
		# df2[instr + '-adjusted-close'] = df[instr + '-adjusted-close']
	
	print(df2.columns)

	df2 = df2[:391902]
	df2.to_csv(new_csv_file, index=False)

	return


instrument_list = [
	# 'AUD_JPY',
	'AUD_USD',
	# 'EUR_AUD',
	# 'EUR_CHF',
	# 'EUR_GBP',
	# 'EUR_JPY',
	'EUR_USD',
	# 'GBP_CHF',
	# 'GBP_JPY',
	'GBP_USD',
	'NZD_USD',
	# 'USD_CAD',
	# 'USD_CHF',
	# 'USD_JPY'
]
csv_file = '1day_pairs1.csv'
# store_multiple_daily_oanda_prices(csv_file, '2010-01-01T00:00:00-00:00', '2020-11-01T0:00:00-00:00', 25, instrument_list, 'D')

# store_multiple_oanda_prices(csv_file, '2010-01-01T00:00:00-00:00', '2020-11-01T0:00:00-00:00', 25, instrument_list, 'D')

# csv_file = '10_min_major_pairs2.csv'
# new_csv_file = '10_min_major_pairs2_adjusted1.csv'
# adjust_data(csv_file, new_csv_file, instrument_list)

# csv_file = '10_min_major_pairs2_adjusted1.csv'
# new_csv_file = '10min_10year_simple1.csv'
# simplify(csv_file, new_csv_file, instrument_list)

fix_index(csv_file)