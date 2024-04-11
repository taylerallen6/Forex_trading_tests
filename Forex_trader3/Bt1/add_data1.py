import backtrader as bt
import numpy as np
import pandas as pd


def diff_log(df):
	return np.log(df) - np.log(df.shift(1))

def diff(df):
	return df - df.shift(1)

def norm_stand(df, zero_to_one=False):
	df = df - df.mean()
	df = df / df.std()
	if zero_to_one:
		df = (df -df.min()) / (df.max() -df.min())
	else:	
		df = (df) / ((df.max() -df.min())/2)
	return df


def format_data(df):

	# Clean NaN values
	df = df.dropna()

	df['date_and_time'] = pd.to_datetime(df['date_and_time'])

	return df


def add_all_data(df, cerebro):

	data = bt.feeds.PandasData(dataname=df,
		# timeframe=bt.feeds.TimeFrame.Minutes,
		# compression=10,
		datetime='date_and_time',
		close='close',
		high='high',
		low='low',
		open='open',
		volume='volume'
		)
	cerebro.adddata(data)

	# for data_name in datas_name_list:
	# 	data = bt.feeds.PandasData(dataname=df[['date_and_time', data_name]],
	# 		datetime='date_and_time',
	# 		close=data_name
	# 		)
	# 	data.plotinfo.plot = False
	# 	cerebro.adddata(data)

	return data