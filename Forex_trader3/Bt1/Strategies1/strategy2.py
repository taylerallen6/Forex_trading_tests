'''
STOP LOSS
'''
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
  params = dict(
    stop_loss=0.02,  # price is 2% less than the entry point
    trail=False,
  )

  def log(self, txt, dt=None):
    '''Logging function for this strategy'''
    dt = dt or self.datas[0].datetime.date(0)
    print('%s, %s' % (dt.isoformat(), txt))

  def notify_order(self, order):
    if not order.status == order.Completed:
      return  # discard any other notification

    if not self.position:  # we left the market
      self.log('CLOSE: {:.4f}'.format(order.executed.price))
      # print('SELL@price: {:.2f}'.format(order.executed.price))
      return

    # We have entered the market
    self.log('BUY: {:.4f}'.format(order.executed.price))
    # print('BUY @price: {:.2f}'.format(order.executed.price))

    if not self.p.trail:
      stop_price = order.executed.price * (1.0 - self.p.stop_loss)
      self.close(exectype=bt.Order.Stop, price=stop_price)
    else:
      self.close(exectype=bt.Order.StopTrail, trailamount=self.p.trail)

  def next(self):
    if not self.position:
      # not in the market and signal triggered
      self.buy()