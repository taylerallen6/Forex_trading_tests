import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# sqlite_file = 'forex2.db'
csv_file = '30_min_major_pairs.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

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

spread_percent = .0002

years = 4

y_window = 144

print("y_window: ", y_window)
print()

df2 = pd.DataFrame()

for instr in instrument_list:

  # df2[instr + '-close'] = df['close']
  open_val = df[instr + '-open']
  volume = df[instr + '-volume']
  # df2[instr + '-range'] = (df['high'] - df['low'])

  ma = open_val.rolling(window=480).mean()
  std = open_val.rolling(window=480).std()
  df2[instr + '-open_adj'] = (open_val - ma) / std

  df2[instr + '-ma_dir'] = ma - ma.shift(240)

  vol_ma = volume.rolling(window=480).mean()
  vol_std = volume.rolling(window=480).std()
  df2[instr + '-volume_adj'] = (volume - vol_ma) / vol_std

  df2[instr + '-diff'] = open_val.diff(periods=144)

  y = open_val.shift(-y_window)
  df2[instr + '-y_diff'] = open_val.diff(periods=y_window).shift(-y_window)


print(df2.columns)

