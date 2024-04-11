import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import empyrical


csv_file = '10_min_major_pairs2_adjusted1.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

split = int(len(df) * .10)
df = df[-split:]

# plt.plot(df['AUD_JPY-adjusted-close'])
# plt.show()

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

for instr in instrument_list:
	plt.plot(df[instr + '-open'])
	plt.plot(df[instr + '-adjusted-open'])
plt.show()

# spread_percent = .0002
# account_val = 1000
# trade_cost = account_val * spread_percent

# years = 4

# day = 144
# y_window = day * 3

# df2 = pd.DataFrame()

# for instr in instrument_list:

#   open_val = df[instr + '-open']
#   volume = df[instr + '-volume']

#   ### NORMLIZED OPEN
#   open_ma = open_val.rolling(window=day).mean()
#   open_std = open_val.rolling(window=day).std()
#   df2[instr + '-open_norm1'] = (open_val - open_ma) / open_std

#   ### NORMLIZED VOLUME
#   vol_ma = volume.rolling(window=day).mean()
#   vol_std = volume.rolling(window=day).std()
#   df2[instr + '-volume_norm1'] = (volume - vol_ma) / vol_std

#   ### NORMLIZED DIFF
#   diff = open_val.diff(periods=day)

#   diff_ma = diff.rolling(window=day).mean()
#   diff_std = diff.rolling(window=day).std()
#   df2[instr + '-diff_norm1'] = (diff - diff_ma) / diff_std

#   ### QUANTITY
#   quantity = account_val / open_val

#   # y = open_val.shift(-y_window)
#   df2[instr + '-y_diff'] = open_val.diff(periods=y_window).shift(-y_window) * quantity

# df2 = df2.dropna()

# x_df = pd.DataFrame()
# y_diff_df = pd.DataFrame()

# for instr in instrument_list:
#   x_df[instr + '-open_norm1'] = df2[instr + '-open_norm1']
#   x_df[instr + '-volume_norm1'] = df2[instr + '-volume_norm1']

#   y_diff_df[instr] = df2[instr + '-y_diff'] - trade_cost
#   y_diff_df[instr + '-short'] = (df2[instr + '-y_diff'] * -1) - trade_cost
#   df2 = df2.drop([instr + '-y_diff'], axis=1)


# print(df2['EUR_USD-open_norm1'])
# plt.plot(df2['EUR_USD-open_norm1'])
# plt.show()