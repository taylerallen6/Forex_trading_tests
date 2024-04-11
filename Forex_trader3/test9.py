import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import empyrical
from datetime import datetime


#############################

###  SCALPING ONLY

#############################

start_time = datetime.now()


csv_file = './10min_10year_simple1.csv'
df = pd.read_csv(csv_file)
df = df.dropna()

split = int(len(df) * .10)
start_point = split * 2
# df = df[-split:]
df = df[start_point:start_point+split]

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
wanted_pct = .0020


def rolling_diff(values):
  # return values.diff(periods=1).mean()
  return values.pct_change(1).mean()


close = df['EUR_USD-close']
high = df['EUR_USD-high']
low = df['EUR_USD-low']

df2['close'] = close

df2['-hour_high'] = high.rolling(5).max()
df2['-hour_low'] = low.rolling(5).min()

df2['-hour_high_diff'] = df2['-hour_high'].rolling(10).apply(rolling_diff)
df2['-hour_low_diff'] = df2['-hour_low'].rolling(10).apply(rolling_diff)
df2['-high_low_calc'] = (df2['-hour_high_diff'] + df2['-hour_low_diff']) / 2

df2['-hour_high_diff2'] = df2['-hour_high'].rolling(20).apply(rolling_diff)
df2['-hour_low_diff2'] = df2['-hour_low'].rolling(20).apply(rolling_diff)
df2['-high_low_calc2'] = (df2['-hour_high_diff2'] + df2['-hour_low_diff2']) / 2

df2['-hour_high_diff3'] = df2['-hour_high'].rolling(30).apply(rolling_diff)
df2['-hour_low_diff3'] = df2['-hour_low'].rolling(30).apply(rolling_diff)
df2['-high_low_calc3'] = (df2['-hour_high_diff3'] + df2['-hour_low_diff3']) / 2

df2['-hour_high_diff4'] = df2['-hour_high'].rolling(40).apply(rolling_diff)
df2['-hour_low_diff4'] = df2['-hour_low'].rolling(40).apply(rolling_diff)
df2['-high_low_calc4'] = (df2['-hour_high_diff4'] + df2['-hour_low_diff4']) / 2

ma = close.rolling(15).mean()
df2['momentum'] = close - ma

df2['pct_change'] = close.pct_change(y_window).shift(-y_window)
df2['y'] = pd.Series(np.zeros(len(close)))
df2.loc[((df2['pct_change'] > wanted_pct)), 'y'] = 1
df2.loc[((df2['pct_change'] < -wanted_pct)), 'y'] = -1

df2 = df2.dropna()


# plt.plot(df2['pct_change'])
# plt.show()

# plt.plot(df2['close'])
# plt.plot(df2['-high_low_calc'])
# plt.plot(df2['-high_low_calc2'])
# plt.plot(df2['-high_low_calc3'])
# plt.plot(df2['-high_low_calc4'])
# plt.show()


x_df = df2[['-high_low_calc', '-high_low_calc2', '-high_low_calc3', '-high_low_calc4', 'momentum']]
y_df = df2['y']


print(x_df.to_numpy().shape)
print(y_df.to_numpy().shape)

x = x_df.to_numpy()
y = y_df.to_numpy()

N, D_in, D_out = len(x), len(x[0]), 1

### DEFINE TRAIN AND TEST DATA
test_length = int(len(x) * .1)
x_train = torch.tensor(x[:-test_length]).float()
x_test = torch.tensor(x[-test_length:]).float()
y_train = torch.tensor(y[:-test_length]).float()
y_test = torch.tensor(y[-test_length:]).float()


dtype = torch.float
device = torch.device("cpu")

class Network1(torch.nn.Module):
  def __init__(self, D_in, D_out):
    super(Network1, self).__init__()
    self.w1 = torch.nn.Parameter(torch.randn(D_in, device=device, dtype=dtype, requires_grad=True))
    self.b1 = torch.nn.Parameter(torch.randn(D_in, device=device, dtype=dtype, requires_grad=True))
    self.w2 = torch.nn.Parameter(torch.randn(D_in, device=device, dtype=dtype, requires_grad=True))

  def forward(self, x):
    y_pred = x * self.w1 + self.b1
    y_pred = torch.tanh(y_pred)
    y_pred = F.linear(y_pred, self.w2)
    y_pred = torch.tanh(y_pred)

    return y_pred


model = Network1(D_in, D_out)

learning_rate = 1e-2
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
criterion = torch.nn.MSELoss(reduction='sum')


### TRAIN
for t in range(10000):
  y_pred = model(x_train)

  loss = criterion(y_pred, y_train)
  if t % 1000 == 999:
    print(t, loss.item())

  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

y_pred = y_pred.detach().numpy()
y_train = y_train.detach().numpy()

y_pred[y_pred > .33] = 1
y_pred[(y_pred <= .33) & (y_pred >= -.33)] = 0
y_pred[y_pred < -.33] = -1

# y_pred[y_pred >= .5] = 1
# y_pred[y_pred < .5] = -1

accuracy = y_pred == y_train
accuracy = accuracy.astype(int)
print("Training accuracy: ", accuracy.mean())


### TEST
y_pred = model(x_test)

loss = criterion(y_pred, y_test)
print("test loss: ", loss.item())

y_pred = y_pred.detach().numpy()
y_test = y_test.detach().numpy()

y_pred[y_pred > .33] = 1
y_pred[(y_pred <= .33) & (y_pred >= -.33)] = 0
y_pred[y_pred < -.33] = -1

# y_pred[y_pred >= .5] = 1
# y_pred[y_pred < .5] = -1

accuracy = y_pred == y_test
accuracy = accuracy.astype(int)
print("Testing accuracy", accuracy.mean())


end_time = datetime.now() - start_time
print()
print("TIME ELAPSED: ", end_time)