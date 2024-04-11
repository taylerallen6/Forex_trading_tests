import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sqlite3

# create connection
conn = sqlite3.connect('../../Python_projects/Forex_AT2/Forex_AT2.db')
c = conn.cursor()


spreadVal = .0002
profitVal = .0003
moveVal = spreadVal + profitVal


df_eurusd = pd.read_csv('^eurusd_price-history-07-31-2018.csv')
df_eurusd.set_index('Time', inplace=True)
df_eurusd.dropna(inplace=True)

c.execute('''SELECT * FROM OandaDataTableD1_5years''',)
retRows = c.fetchall()
df_oanda_eurusd = pd.DataFrame(retRows, columns=['Datetime', 'Frequency', 'Close', 'High', 'Low', 'Open', 'Volume'])
df_oanda_eurusd.set_index('Datetime', inplace=True)
df_oanda_eurusd.dropna(inplace=True)
# print(df_oanda_eurusd.head())



def step():
	df_eurusd['Returns'] = np.where(df_eurusd['High']-df_eurusd['Open'] >= moveVal, profitVal, df_eurusd['Last']-df_eurusd['Open']-spreadVal)

def oanda_step():
	df_oanda_eurusd['Returns'] = np.where(df_oanda_eurusd['High']-df_oanda_eurusd['Open'] >= moveVal, profitVal, df_oanda_eurusd['Close']-df_oanda_eurusd['Open']-spreadVal)


print()

step()
csvReturns = np.array(df_eurusd['Returns'])
print("csv returns: ", csvReturns.sum())

oanda_step()
oandaReturns = np.array(df_oanda_eurusd['Returns'])
startVal = int(len(oandaReturns)/5)*4
print('test data length: ', len(oandaReturns) - startVal)
print("oanda returns: ", oandaReturns[startVal:].sum())



# close connection
conn.close()