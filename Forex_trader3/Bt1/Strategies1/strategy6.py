'''
Successful moving average direction strategy
'''

from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt
import backtrader.indicators as btind

from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import random


# Create a Strategy
class TestStrategy(bt.Strategy):
  # params = (
  #   ('period', 15),
  #   )
  params = dict(
      period=20,
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

    # My variables
    self.y_window = 200
    self.ma_period = 1580
    self.dir_period = 440
    self.range_period = 20
    self.trade_date = None
    self.trade_days = 0
    self.can_trade = False

    self.stop_orders = []

    self.account_values = []
    self.actual_account_val = 0

    # Add a MovingAverageSimple indicator
    self.sma_daily = btind.SMA(self.data, period=self.ma_period)
    sma_high = btind.SMA(self.data1.high, period=self.range_period)
    sma_low = btind.SMA(self.data1.low, period=self.range_period)
    self.range = sma_high - sma_low

    self.add_timer(
      when=bt.timer.SESSION_START,
      offset=datetime.timedelta(),
      repeat=datetime.timedelta(),
      weekdays=[],
    )

  
  def notify_cashvalue(self, cash, value):
    self.actual_account_val = value


  def notify_order(self, order):
    if order.exectype == 4 or order.exectype == 3:
      if order not in self.stop_orders:
        self.stop_orders.append(order)

    if order.status in [order.Submitted, order.Accepted]:
      # Buy/Sell order submitted/accepted to/by broker - Nothing to do
      return

    if not order.status == order.Completed:
      return  # discard any other notification

    # if order.status in [order.Completed]:
    #   if order.isbuy():
    #     # self.log(
    #     #   'BUY EXECUTED, Price: %.5f, Cost: %.2f, Comm: %.2f' % (
    #     #     order.executed.price,
    #     #     order.executed.value,
    #     #     order.executed.comm))

    #     stop_loss_price = order.executed.price - (self.range * 2)
    #     self.close(exectype=bt.Order.Stop, price=stop_loss_price)
    #     take_profit_price = order.executed.price + (self.range * 2)
    #     self.close(exectype=bt.Order.StopLimit, price=take_profit_price)

    #   else: # is sell order
    #     # self.log('SELL EXECUTED, Price: %.5f, Cost: %.2f, Comm: %.2f' % (
    #     #   order.executed.price,
    #     #   order.executed.value,
    #     #   order.executed.comm))
        
    #     stop_loss_price = order.executed.price + (self.range * 2)
    #     self.close(exectype=bt.Order.Stop, price=stop_loss_price)
    #     take_profit_price = order.executed.price - (self.range * 2)
    #     self.close(exectype=bt.Order.StopLimit, price=take_profit_price)

    if order.status in [order.Canceled, order.Margin, order.Rejected]:
      self.log('Order Canceled/Margin/Rejected')

    # Write down: no pending order
    self.order = None

    if not self.position:  # we left the market
      # self.log('CLOSE: {:.4f}'.format(order.executed.price))
      # print('SELL@price: {:.2f}'.format(order.executed.price))
      return
    

  def notify_trade(self, trade):
    if not trade.isclosed:
      return

    # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (
    #   trade.pnl,
    #   trade.pnlcomm))

    self.log('account: %.2f' % (self.actual_account_val))
    self.account_values.append(self.actual_account_val)
    # print()


  def notify_timer(self, timer, when, *args, **kwargs):
    if not self.position:
      self.can_trade = True
      # self.log("NOTIFY TIMER")

  def next(self):

    #   #Check if an order is pending.. if yes, cant send 2nd order
    if self.order:
      return

    if not self.position:
      for order in self.stop_orders:
        self.cancel(order)

    # If in  trade
    if self.position:
      time_diff = self.data1.datetime.date(0) - self.trade_date
      self.trade_days = (time_diff.days * 24 * 60) / 10

      if self.trade_days >= self.y_window:
        # self.log('EXIT CREATED, %.2f' % self.dataclose[0])
        self.order = self.close()

    # if self.can_trade:
    #   self.can_trade = False
      
    # If not in trade
    if not self.position:
      
      if self.sma_daily[0] < self.sma_daily[-self.dir_period] and self.dataclose[0] > self.sma_daily[0]:
        self.order = self.buy()

        self.trade_days = 0
        self.trade_date = self.data1.datetime.date(0)
      
      elif self.sma_daily[0] > self.sma_daily[-self.dir_period] and self.dataclose[0] < self.sma_daily[0]:
        self.order = self.sell()
      
        self.trade_days = 0
        self.trade_date = self.data1.datetime.date(0)

      
