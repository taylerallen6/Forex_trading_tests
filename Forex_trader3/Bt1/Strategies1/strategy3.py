from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class TestStrategy(bt.Strategy):
  params = (
    ('period', 10),
    ('onlydaily', False),
  )

  def __init__(self):
    self.sma_small_tf = btind.SMA(self.data, period=self.p.period)
    self.sma_large_tf = btind.SMA(self.data1, period=self.p.period)

  def nextstart(self):
    print('--------------------------------------------------')
    print('nextstart called with len', len(self))
    print('--------------------------------------------------')

    super(TestStrategy, self).nextstart()