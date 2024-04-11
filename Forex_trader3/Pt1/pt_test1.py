# -*- coding: utf-8 -*-
import torch

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlalchemy as db


sqlite_file = '../forex2.db'
# sqlite_file = '10_min_forex.db'
engine = db.create_engine('sqlite:///'+ sqlite_file)
conn = engine.connect()

currency_pair = 'eur_usd1'
spread_val = .0002

query_val = 1000000000
sql = "SELECT * FROM {} WHERE rowid <= {}".format(currency_pair, query_val)
df = pd.read_sql(sql, conn, parse_dates=['date_and_time'])

y_window = 1

print("currency_pair: ", currency_pair)
print("y_window: ", y_window)
print()

df2 = pd.DataFrame()
df2['date_and_time'] = df['date_and_time']
df2['close'] = df['close']
df2['open'] = df['open']

df2['ma'] = df2['close'].rolling(window=5).mean()
df2['std'] = df2['close'].rolling(window=5).std()
df2['close_adj'] = (df2['close'] - df2['ma']) / df2['std']

df2['y'] = df2['close'].shift(-y_window)
df2['y_diff'] = df2['close'].diff(periods=y_window).shift(-y_window)

df2 = df2.dropna()

# plt.plot(df2['close_adj'])
# plt.show()

# print(df2[['close', 'close_adj', 'y', 'y_diff']].head(10))


def rolling_window(a, window, step_size):
  shape = a.shape[:-1] + (a.shape[-1] - window + 1 - step_size + 1, window)
  strides = a.strides + (a.strides[-1] * step_size,)
  return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

window = 20
x = df2['close_adj'].to_numpy()
x = rolling_window(x, window, 1)
y = df2['y_diff'].to_numpy()[window-1:]
y = y.reshape((len(y), 1))
y = y * 100


# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = len(y), window, 100, 1

# Create random Tensors to hold inputs and outputs
test_length = 200
x_train = torch.tensor(x[:-test_length]).float()
y_train = torch.tensor(y[:-test_length]).float()
x_test = torch.tensor(x[-test_length:]).float()
y_test = torch.tensor(y[-test_length:]).float()


# Use the nn package to define our model and loss function.
model = torch.nn.Sequential(
  torch.nn.Linear(D_in, H),
  torch.nn.ReLU(),
  torch.nn.Linear(H, D_out),
)
loss_fn = torch.nn.MSELoss(reduction='sum')

learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(5000):
  y_pred = model(x_train)

  loss = loss_fn(y_pred, y_train)
  if t % 100 == 99:
    print(t, loss.item())

  optimizer.zero_grad()
  loss.backward()
  optimizer.step()


y_pred = model(x_test)
loss = loss_fn(y_pred, y_test)
print("test loss: ", loss.item())

plt.plot(y_test.detach().numpy())
plt.plot(y_pred.detach().numpy())
plt.show()