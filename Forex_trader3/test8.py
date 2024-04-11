import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import empyrical


#############################

###  SCALPING ONLY

#############################


csv_file = './10min_10year_simple1.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

split = int(len(df) * .01)
df = df[-split:]

instrument_list = [
	'AUD_USD',
	'EUR_USD',
	'GBP_USD',
	'NZD_USD',
]


df2 = pd.DataFrame()

years = 10.5
day = 144
y_window = 5
sl_window = 2

spread_percent = .0002
wanted_pct = .002


close = df['EUR_USD-close']


# ### PERCENT PROFIT LONG
# max_y = close.rolling(window=y_window).max().shift(-y_window)
# pct_profit_long = (max_y - close) / close

# ### PERCENT PROFIT SHORT
# min_y = close.rolling(window=y_window).min().shift(-y_window)
# pct_profit_short = -((min_y - close) / close)

# ### PERCENT LOSS LONG
# min_y = close.rolling(window=sl_window).min().shift(-sl_window)
# pct_loss_long = (min_y - close) / close

# ### PERCENT LOSS SHORT
# max_y = close.rolling(window=sl_window).max().shift(-sl_window)
# pct_loss_short = -((max_y - close) / close)

# ### PERCENT RETURN LONG
# df2['pct_return_long'] = pct_loss_long
# print(df2['pct_return_long'].head(10))
# # inds = df2['pct_return_long'].index[pct_return_long > 0]
# # print(inds)
# # print(pct_return_long.head(10))

# df2['pct_return_long'].loc[(pct_loss_long > 0), 'pct_return_long'] = pct_profit_long[pct_loss_long > 0]
# print(df2['pct_return_long'].head(10))

# # pct_return_long.replace([inds], pct_profit_long.iloc[inds].tolist())
# # print(pct_return_long.head(10))



df2 = df2.dropna()


# plt.plot(df2['close'])
# plt.plot(df2['ma'])

# # df2['direction'] = np.random.randint(2, size=len(df2['y_diff']))
# df2['direction'] = np.zeros(len(df2['y_diff']))
# df2.loc[((df2['ma_dir'] > 0) & (df2['close'] < df2['ma'])), 'direction'] = 1
# df2.loc[((df2['ma_dir'] < 0) & (df2['close'] > df2['ma'])), 'direction'] = -1

# df2['return'] = df2['y_diff'] * df2['direction']

# # ### PROFIT
# df2['profit'] = (df2['return'] - trade_cost)
# # stop_loss = -2000
# # df2.loc[df2['profit'] < stop_loss, 'profit'] = stop_loss
# # plt.scatter(range(len(df2['profit'])), df2['profit'])
# # plt.show()
# df2['cumsum'] = df2['profit'].cumsum()

# print("average: ", df2['profit'].mean())
# print("average profit: ", df2[df2['profit'] > 0]['profit'].mean())
# print("average loss: ", df2[df2['profit'] < 0]['profit'].mean())
# print("min: ", df2['profit'].min())
# print("max: ", df2['profit'].max())
# # print("avg range: ", df2['range'].mean())

# estimated_profit = df2['profit'].sum() / y_window / years / 12
# print("avg monthly profit: ", estimated_profit)
# print("avg monthly after tax: ", estimated_profit * .75)

# numb_of_trades = len(df2['profit']) / y_window / years
# print('Number of trades per year: ', numb_of_trades)


# # ### PLOT
# plt.plot(df2['cumsum'])
# plt.show()