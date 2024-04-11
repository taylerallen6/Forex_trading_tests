import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import empyrical


# sqlite_file = 'forex2.db'
csv_file = '../30_min_major_pairs.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

# df = df[:-20000]

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
account_val = 1000
trade_cost = account_val * spread_percent

years = 4

y_window = 144
day = 48

df2 = pd.DataFrame()

for instr in instrument_list:

  # df2[instr + '-close'] = df['close']
  open_val = df[instr + '-open']
  # df2[instr + '-open'] = open_val
  volume = df[instr + '-volume']
  # df2[instr + '-range'] = (df['high'] - df['low'])

  ### ADJUSTED OPEN
  # ma = open_val.rolling(window=day).mean()
  # std = open_val.rolling(window=day).std()
  # df2[instr + '-open_adj1'] = (open_val - ma) / std

  # ma = open_val.rolling(window=day * 2).mean()
  # std = open_val.rolling(window=day * 2).std()
  # df2[instr + '-open_adj2'] = (open_val - ma) / std

  # ma = open_val.rolling(window=day * 3).mean()
  # std = open_val.rolling(window=day * 3).std()
  # df2[instr + '-open_adj3'] = (open_val - ma) / std

  # ma = open_val.rolling(window=day * 4).mean()
  # std = open_val.rolling(window=day * 4).std()
  # df2[instr + '-open_adj4'] = (open_val - ma) / std

  # ma = open_val.rolling(window=day * 5).mean()
  # std = open_val.rolling(window=day * 5).std()
  # df2[instr + '-open_adj5'] = (open_val - ma) / std

  # df2[instr + '-ma_dir'] = ma - ma.shift(240)

  ### ADJUSTED VOLUME
  vol_ma = volume.rolling(window=day).mean()
  vol_std = volume.rolling(window=day).std()
  df2[instr + '-volume_adj1'] = (volume - vol_ma) / vol_std

  # vol_ma = volume.rolling(window=day * 2).mean()
  # vol_std = volume.rolling(window=day * 2).std()
  # df2[instr + '-volume_adj2'] = (volume - vol_ma) / vol_std

  # vol_ma = volume.rolling(window=day * 3).mean()
  # vol_std = volume.rolling(window=day * 3).std()
  # df2[instr + '-volume_adj3'] = (volume - vol_ma) / vol_std

  # vol_ma = volume.rolling(window=day * 4).mean()
  # vol_std = volume.rolling(window=day * 4).std()
  # df2[instr + '-volume_adj4'] = (volume - vol_ma) / vol_std

  # vol_ma = volume.rolling(window=day * 5).mean()
  # vol_std = volume.rolling(window=day * 5).std()
  # df2[instr + '-volume_adj5'] = (volume - vol_ma) / vol_std

  ### ADJUSTED DIFF
  diff = open_val.diff(periods=day)

  diff_ma = diff.rolling(window=day).mean()
  diff_std = diff.rolling(window=day).std()
  df2[instr + '-diff_adj1'] = (diff - diff_ma) / diff_std

  # diff_ma = diff.rolling(window=day * 2).mean()
  # diff_std = diff.rolling(window=day * 2).std()
  # df2[instr + '-diff_adj2'] = (diff - diff_ma) / diff_std

  # diff_ma = diff.rolling(window=day * 3).mean()
  # diff_std = diff.rolling(window=day * 3).std()
  # df2[instr + '-diff_adj3'] = (diff - diff_ma) / diff_std

  # diff_ma = diff.rolling(window=day * 4).mean()
  # diff_std = diff.rolling(window=day * 4).std()
  # df2[instr + '-diff_adj4'] = (diff - diff_ma) / diff_std

  # diff_ma = diff.rolling(window=day * 5).mean()
  # diff_std = diff.rolling(window=day * 5).std()
  # df2[instr + '-diff_adj5'] = (diff - diff_ma) / diff_std

  quantity = account_val / open_val

  # y = open_val.shift(-y_window)
  df2[instr + '-y_diff'] = open_val.diff(periods=y_window).shift(-y_window) * quantity

df2 = df2.dropna()

y_diff_df = pd.DataFrame()

for instr in instrument_list:
  y_diff_df[instr] = df2[instr + '-y_diff'] - trade_cost
  y_diff_df[instr + '-short'] = (df2[instr + '-y_diff'] * -1) - trade_cost
  df2 = df2.drop([instr + '-y_diff'], axis=1)

# print(df2.columns)


print(df2.to_numpy().shape)
print(y_diff_df.to_numpy().shape)

x = df2.to_numpy()
returns = y_diff_df.to_numpy()

### N is batch size; D_in is input dimension;
### H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = len(x), len(x[0]), 10, len(instrument_list * 2)

### DEFINE TRAIN AND TEST DATA
test_length = 10000
x_train = torch.tensor(x[:-test_length]).float()
x_test = torch.tensor(x[-test_length:]).float()
returns_train = torch.tensor(returns[:-test_length]).float()
returns_test = torch.tensor(returns[-test_length:]).float()


### NEURAL NETWORK MODEL
model = torch.nn.Sequential(
  torch.nn.Linear(D_in, H),
  torch.nn.ReLU(),
  torch.nn.Linear(H, H),
  torch.nn.ReLU(),
  torch.nn.Linear(H, D_out),
  torch.nn.Softmax(dim=1)
)
count = 0
for parameter in model.parameters():
  parameter.requires_grad = False
  # print(parameter)
  if count == 0:
    break

# loss_fn = torch.nn.MSELoss(reduction='sum')
learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

def run_model(x, returns):
  y_pred = model(x)
  print(y_pred.shape)
  print(returns.shape)
  returns = y_pred * returns
  returns = returns.sum(1) / y_window
  print(returns.shape)
  # y_pred = ((returns.mean() - 0) / returns.std())
  y_pred = returns

  return y_pred, returns


### TRAIN
for t in range(1000):
  y_pred, returns = run_model(x_train, returns_train)

  loss = y_pred.sum() * -1
  if t % 100 == 99:
    print(t, loss.item())

  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

plt.plot(returns.detach().numpy().cumsum())
plt.show()


### TEST
y_pred, returns = run_model(x_test, returns_test)

loss = y_pred.sum() * -1
print("test loss: ", loss.item())

plt.plot(returns.detach().numpy().cumsum())
plt.show()

