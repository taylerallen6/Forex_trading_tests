import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlalchemy as db


sqlite_file = 'forex2.db'
# sqlite_file = '10_min_forex.db'
engine = db.create_engine('sqlite:///'+ sqlite_file)
conn = engine.connect()

currency_pair = 'eur_usd1'
spread_val = .0002
# currency_pair = 'usd_jpy1'
# spread_val = .02
# currency_pair = 'usd_cad1'
# spread_val = .0003
# currency_pair = 'gbp_usd1'

query_val = 1000000000
sql = "SELECT * FROM {} WHERE rowid <= {}".format(currency_pair, query_val)
df = pd.read_sql(sql, conn, parse_dates=['date_and_time'])

years = 4

y_window = 5
period = 15


print("currency_pair: ", currency_pair)
print("y_window: ", y_window)
print("mov_avg_period: ", period)
print()

df2 = pd.DataFrame()
# df2['date_and_time'] = df['date_and_time']
df2['close'] = df['close']
df2['open'] = df['open']
df2['range'] = (df['high'] - df['low'])
# df2['range_avg'] = df2['range'].rolling(window=range_period).mean().shift(range_period)

df2['mov_avg'] = df2['close'].rolling(window=period).mean()
df2['std'] = df2['close'].rolling(window=period).std()
# df2['close_adj'] = ((df['close'] - df2['mov_avg']) / df2['std']) /3

df2['y'] = df2['close'].shift(-y_window)
# df2['y_diff'] = df2['y'].diff(periods=y_window)
df2['y_diff'] = df2['close'].diff(periods=y_window).shift(-y_window)

df2['quantity'] = 1000 / df2['close']


df2 = df2.dropna()


# df2['direction'] = np.random.randint(2, size=len(df2['y_diff']))
df2['direction'] = np.zeros(len(df2['y_diff']))
df2.loc[df2['close'] < df2['mov_avg'], 'direction'] = 1

df2['return'] = df2['y_diff']
df2.loc[df2['direction'] == 0, 'return'] *= -1
# stop_loss = (-40 * spread_val) - (5 * spread_val)
# stop_loss = df2['close'] * (1.0 - 0.1)
# df2.loc[df2['return'] < stop_loss, 'return'] = stop_loss

### PROFIT
df2['profit'] = (df2['return'] - spread_val) * df2['quantity'] * 20
df2['cumsum'] = df2['profit'].cumsum()

print("average: ", df2['profit'].mean())
print("min: ", df2['profit'].min())
print("max: ", df2['profit'].max())
print("avg range: ", df2['range'].mean())

estimated_profit = df2['profit'].sum() / y_window / years / 12
print("avg monthly profit: ", estimated_profit)

print("avg monthly after tax: ", estimated_profit * .75)


### PLOT
plt.plot(df2['cumsum'])
plt.show()