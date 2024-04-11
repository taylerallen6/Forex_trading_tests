from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


# Create a Strategy
class TestStrategy(bt.Strategy):
	params = (
		('maperiod', 15),
		)

	def log(self, txt, dt=None):
		'''Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		# Keep a reference to the "close" line in the data[0] dataseries
		self.dataclose = self.datas[0].close

		# To keep trace of pending orders and buy price/commision
		self.order = None
		self.buyprice = None
		self.buycomm = None

		# Add a MovingAverageSimple indicator
		self.sma = bt.indicators.SimpleMovingAverage(
			self.datas[0], period=self.params.maperiod)
    
		# Number of days in trade
		self.y_window = 5
		self.trade_date = None
		self.trade_days = 0

	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
			# Buy/Sell order submitted/accepted to/by broker - Nothing to do
			return

		# Check if an order has been completed
		# Attention: broker could reject order if not enough cash
		if order.status in [order.Completed]:
			if order.isbuy():
				self.log(
					'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % (
						order.executed.price,
						order.executed.value,
						order.executed.comm))

				self.buyprice = order.executed.price
				self.buycomm = order.executed.comm

			else: # is sell order
				self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % (
					order.executed.price,
					order.executed.value,
					order.executed.comm))

			self.bar_executed = len(self)

		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		# Write down: no pending order
		self.order = None


	def notify_trade(self, trade):
		if not trade.isclosed:
			return

		self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (
			trade.pnl,
			trade.pnlcomm))

	def next(self):
		# Simply log the closing price of the series from the reference
		# self.log('Close, %.2f' % self.dataclose[0])

		#Check if an order is pending.. if yes, cant send 2nd order
		if self.order:
			return

		# If in  trade
		if self.position:
			self.trade_days += 1

			# if (self.datas[0].datetime.date(0) - self.trade_date) == self.y_window:
			if self.trade_days >= self.y_window:
				self.log('EXIT CREATED, %.2f' % self.dataclose[0])
				self.order = self.close()

				self.trade_days = 0
		
		# If not in trade
		elif not self.position:
			# self.log('BUY CREATED, %.2f' % self.dataclose[0])
			# # Keep track of the created order to avoid a 2nd order
			# self.order = self.buy()

			if self.dataclose[0] < self.sma[0]:
				# BUY!
				self.log('BUY CREATED, %.2f' % self.dataclose[0])
				# Keep track of the created order to avoid a 2nd order
				self.order = self.buy()
				
			elif self.dataclose[0] > self.sma[0]:
				# Sell
				self.log('SELL CREATED, %.2f' % self.dataclose[0])
				# Keep track of the created order to avoid a 2nd order
				self.order = self.sell()
			
			# self.trade_date = self.datas[0].datetime.date(0)
			
