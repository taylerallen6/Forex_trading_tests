import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import empyrical


csv_file = '10_min_major_pairs2_adjusted1.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

split = int(len(df) * 1.0)
df = df[-split:]

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


df2 = pd.DataFrame()

years = 10.5
day = 144
y_window = 10 * day

spread_percent = .0002
account_val = 100000
trade_cost = account_val * spread_percent

df2['close'] = df['EUR_USD-close']
df2['adj_close'] = df['EUR_USD-adjusted-close']
# df2['open'] = df['EUR_USD-adjusted-open']
# df2['range'] = (df['high'] - df['low'])
# df2['range_avg'] = df2['range'].rolling(window=20).mean()

df2['ma'] = df2['close'].rolling(window=40 * day).mean()
df2['ma_dir'] = df2['ma'] - df2['ma'].shift(30 * day)
# df2['std'] = df2['close'].rolling(window=15).std()
# df2['close_adj'] = (df2['close'] - df2['ma']) / df2['range_avg']

df2['y'] = df2['close'].shift(-y_window)
df2['y_diff'] = df2['close'].diff(periods=y_window).shift(-y_window)

quantity = account_val / df2['adj_close']
df2['y_diff'] = df2['adj_close'].diff(periods=y_window).shift(-y_window) * quantity

# print(df2[['ma', 'ma_dir']].head(10))

df2 = df2.dropna()


# df3 = df2[df2['ma_dir'] < 0][df2['close'] > df2['ma']]


plt.plot(df2['close'])
plt.plot(df2['ma'])
# plt.plot(df3['y_diff'].cumsum())
plt.show()


# df2['direction'] = np.random.randint(2, size=len(df2['y_diff']))
df2['direction'] = np.zeros(len(df2['y_diff']))
df2.loc[((df2['ma_dir'] > 0) & (df2['close'] < df2['ma'])), 'direction'] = 1
df2.loc[((df2['ma_dir'] < 0) & (df2['close'] > df2['ma'])), 'direction'] = -1

df2['return'] = df2['y_diff'] * df2['direction']

# ### PROFIT
df2['profit'] = (df2['return'] - trade_cost)
# stop_loss = -2000
# df2.loc[df2['profit'] < stop_loss, 'profit'] = stop_loss
# plt.scatter(range(len(df2['profit'])), df2['profit'])
# plt.show()
df2['cumsum'] = df2['profit'].cumsum()

print("average: ", df2['profit'].mean())
print("average profit: ", df2[df2['profit'] > 0]['profit'].mean())
print("average loss: ", df2[df2['profit'] < 0]['profit'].mean())
print("min: ", df2['profit'].min())
print("max: ", df2['profit'].max())
# print("avg range: ", df2['range'].mean())

estimated_profit = df2['profit'].sum() / y_window / years / 12
print("avg monthly profit: ", estimated_profit)
print("avg monthly after tax: ", estimated_profit * .75)

numb_of_trades = len(df2['profit']) / y_window / years
print('Number of trades per year: ', numb_of_trades)


# ### PLOT
plt.plot(df2['cumsum'])
plt.show()