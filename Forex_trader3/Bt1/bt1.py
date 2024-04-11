from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

from . import add_data1 as add_data
from .Strategies1.strategy5 import TestStrategy as Strategy


class FixedCommisionScheme(bt.CommInfoBase):
	'''
	This is a simple fixed commission scheme
	'''
	params = (
		('pip', 0.00014),
		('commission', 0),
		('stocklike', True),
		('commtype', bt.CommInfoBase.COMM_FIXED),
		)

	def _getcommission(self, size, price, pseudoexec):
		return self.p.commission + (abs(size) * self.p.pip)


def run_bt(df):

	cerebro = bt.Cerebro()
	cerebro.addstrategy(Strategy)

	# Create a Data Feed
	df = add_data.format_data(df)
	data = bt.feeds.PandasData(dataname=df,
		timeframe=bt.feeds.TimeFrame.Minutes,
		compression=10,
		datetime='date_and_time',
		close='close',
		high='high',
		low='low',
		open='open',
		volume='volume'
		)
	cerebro.adddata(data)
	
	cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)

	cerebro.broker.setcash(200000.0) # 10000
	cerebro.addsizer(bt.sizers.FixedSize, stake=30000)
	# cerebro.broker.setcommission(commission=0.0)
	cerebro.broker.setcommission(commission=0.0001)
	# cerebro.broker.setcommission(commission=0.05, stocklike=True, commtype=bt.CommInfoBase.COMM_FIXED)

	# comminfo = FixedCommisionScheme()
	# cerebro.broker.addcommissioninfo(comminfo)

	print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
	stats = cerebro.run()
	print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

	# Plot the result
	# cerebro.plot()
	
	account_values = stats[0].account_values
	# pred_diffs = stats[0].pred_diffs
	stats = [
		account_values,
		# pred_diffs,
		]

	return stats