import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import empyrical


csv_file = '10_min_major_pairs2_adjusted1.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

split = int(len(df) * .5)
df = df[-split:]

instrument_list = [
	'AUD_JPY',
	# 'AUD_USD',
	# 'EUR_AUD',
	# 'EUR_CHF',
	# 'EUR_GBP',
	# 'EUR_JPY',
	# 'EUR_USD',
	# 'GBP_CHF',
	# 'GBP_JPY',
	# 'GBP_USD',
	# 'NZD_USD',
	# 'USD_CAD',
	# 'USD_CHF',
	# 'USD_JPY'
]

spread_percent = .0002
account_val = 1000
trade_cost = account_val * spread_percent

years = 4

day = 144
y_window = day * 3
# y_window = 3

df2 = pd.DataFrame()

def rolling_diff(values):
  return values.diff(periods=1).mean()

for instr in instrument_list:

  open_val = df[instr + '-open']
  high = df[instr + '-high']
  low = df[instr + '-low']
  # df2[instr + '-high'] = df[instr + '-high']
  # df2[instr + '-low'] = df[instr + '-low']

  adjusted_open = df[instr + '-adjusted-open']

  df2[instr + '-hour_high'] = high.rolling(6).max()
  df2[instr + '-hour_low'] = low.rolling(6).min()
  # df2[instr + '-5hour_high'] = high.rolling(6*5).max()
  # df2[instr + '-5hour_low'] = low.rolling(6*5).min()

  # df2[instr + '-rolling_apply'] = high.rolling(10).apply(rolling_diff)
  df2[instr + '-hour_high_diff'] = df2[instr + '-hour_high'].rolling(10).apply(rolling_diff)
  df2[instr + '-hour_low_diff'] = df2[instr + '-hour_low'].rolling(10).apply(rolling_diff)
  df2[instr + '-high_low_calc'] = (df2[instr + '-hour_high_diff'] + df2[instr + '-hour_low_diff']) / 2

  df2[instr + '-hour_high_diff2'] = df2[instr + '-hour_high'].rolling(20).apply(rolling_diff)
  df2[instr + '-hour_low_diff2'] = df2[instr + '-hour_low'].rolling(20).apply(rolling_diff)
  df2[instr + '-high_low_calc2'] = (df2[instr + '-hour_high_diff'] + df2[instr + '-hour_low_diff']) / 2

  df2[instr + '-hour_high_diff3'] = df2[instr + '-hour_high'].rolling(30).apply(rolling_diff)
  df2[instr + '-hour_low_diff3'] = df2[instr + '-hour_low'].rolling(30).apply(rolling_diff)
  df2[instr + '-high_low_calc3'] = (df2[instr + '-hour_high_diff'] + df2[instr + '-hour_low_diff']) / 2

  df2[instr + '-hour_high_diff4'] = df2[instr + '-hour_high'].rolling(40).apply(rolling_diff)
  df2[instr + '-hour_low_diff4'] = df2[instr + '-hour_low'].rolling(40).apply(rolling_diff)
  df2[instr + '-high_low_calc4'] = (df2[instr + '-hour_high_diff'] + df2[instr + '-hour_low_diff']) / 2


  ### QUANTITY
  quantity = account_val / adjusted_open

  df2[instr + '-y_diff'] = adjusted_open.diff(periods=y_window).shift(-y_window) * quantity

df2 = df2.dropna()

# for instr in instrument_list:
#   # plt.plot(df[instr + '-adjusted-open'])
#   plt.plot(df2[instr + '-high'])
#   plt.plot(df2[instr + '-low'])
#   plt.plot(df2[instr + '-hour_high'])
#   plt.plot(df2[instr + '-hour_low'])
#   plt.plot(df2[instr + '-5hour_high'])
#   plt.plot(df2[instr + '-5hour_low'])
#   # plt.plot(df2[instr + '-hour_high_diff'])
#   # plt.plot(df2[instr + '-hour_low_diff'])
#   # plt.plot(df2[instr + '-high_low_calc'])
# plt.show()

for instr in instrument_list:
  plt.plot(df2[instr + '-y_diff'])
plt.show()


x_df = pd.DataFrame()
y_diff_df = pd.DataFrame()

for instr in instrument_list:
  x_df[instr + '-hour_high_diff'] = df2[instr + '-hour_high_diff']
  x_df[instr + '-hour_low_diff'] = df2[instr + '-hour_low_diff']
  x_df[instr + '-high_low_calc'] = df2[instr + '-high_low_calc']

  x_df[instr + '-hour_high_diff2'] = df2[instr + '-hour_high_diff2']
  x_df[instr + '-hour_low_diff2'] = df2[instr + '-hour_low_diff2']
  x_df[instr + '-high_low_calc2'] = df2[instr + '-high_low_calc2']

  x_df[instr + '-hour_high_diff3'] = df2[instr + '-hour_high_diff3']
  x_df[instr + '-hour_low_diff3'] = df2[instr + '-hour_low_diff3']
  x_df[instr + '-high_low_calc3'] = df2[instr + '-high_low_calc3']

  x_df[instr + '-hour_high_diff4'] = df2[instr + '-hour_high_diff4']
  x_df[instr + '-hour_low_diff4'] = df2[instr + '-hour_low_diff4']
  x_df[instr + '-high_low_calc4'] = df2[instr + '-high_low_calc4']

  y_diff_df[instr] = df2[instr + '-y_diff']
  # y_diff_df[instr + '-short'] = (df2[instr + '-y_diff'] * -1)
  # df2 = df2.drop([instr + '-y_diff'], axis=1)


# print(df2['EUR_USD-open_norm1'])
# plt.plot(df2['EUR_USD-open_norm1'])
# plt.show()

print(x_df.to_numpy().shape)
print(y_diff_df.to_numpy().shape)

x = x_df.to_numpy()
returns = y_diff_df.to_numpy()

### N is batch size; D_in is input dimension;
### H is hidden dimension; D_out is output dimension.
N, D_in, D_out = len(x), len(x[0]), 1

### DEFINE TRAIN AND TEST DATA
test_length = int(len(x) * .1)
x_train = torch.tensor(x[:-test_length]).float()
x_test = torch.tensor(x[-test_length:]).float()
returns_train = torch.tensor(returns[:-test_length]).float()
returns_test = torch.tensor(returns[-test_length:]).float()


dtype = torch.float
device = torch.device("cpu")

class Network1(torch.nn.Module):
  def __init__(self, D_in, D_out):
    super(Network1, self).__init__()
    self.w1 = torch.nn.Parameter(torch.randn(D_in, device=device, dtype=dtype, requires_grad=True))
    self.b1 = torch.nn.Parameter(torch.randn(D_in, device=device, dtype=dtype, requires_grad=True))
    self.w2 = torch.nn.Parameter(torch.randn(D_out, D_in, device=device, dtype=dtype, requires_grad=True))

  def forward(self, x):
    y_pred = x * self.w1 + self.b1
    y_pred = torch.tanh(y_pred)
    y_pred = F.linear(y_pred, self.w2)
    y_pred = torch.tanh(y_pred)

    return y_pred


model = Network1(D_in, D_out)

learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


def run_model(x, returns):
  y_pred = model(x)
  returns = (y_pred * returns) - (abs(y_pred) * trade_cost)
  returns = returns.sum(1) / y_window
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
