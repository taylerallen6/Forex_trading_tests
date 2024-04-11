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

split = int(len(df) * .1)
start_point = split * 2
df = df[-split:]
# df = df[start_point:start_point+split]

instrument_list = [
	'AUD_USD',
	'EUR_USD',
	'GBP_USD',
	'NZD_USD',
]


df2 = pd.DataFrame()

years = 10.5
day = 144
hour = 6
y_window = 5

spread_percent = .0002
wanted_pct = .001


close = df['EUR_USD-close']
high = df['EUR_USD-high']
low = df['EUR_USD-low']

df2['close'] = close

df2['high1'] = high.rolling(hour).max()
df2['low1'] = low.rolling(hour).min()
df2['high2'] = high.rolling(hour*2).max()
df2['low2'] = low.rolling(hour*2).min()
df2['high3'] = high.rolling(hour*3).max()
df2['low3'] = low.rolling(hour*3).min()
df2['high4'] = high.rolling(hour*4).max()
df2['low4'] = low.rolling(hour*4).min()
df2['high5'] = high.rolling(hour*5).max()
df2['low5'] = low.rolling(hour*5).min()

# df2['high1_pct'] = 


# ma = close.rolling(15).mean()
# df2['momentum'] = close - ma

df2['pct_change'] = close.pct_change(y_window).shift(-y_window)
# df2['y'] = np.zeros(len(close))
# df2.loc[((df2['pct_change'] > wanted_pct)), 'y'] = 1
# df2.loc[((df2['pct_change'] < -wanted_pct)), 'y'] = -1

df2 = df2.dropna()

# print(df2.head(20))


# plt.plot(df2['pct_change'])
# plt.show()

# plt.plot(df2['close'])
# plt.plot(df2['pct_change'])
# plt.plot(df2['high1'])
# plt.plot(df2['low1'])
# plt.plot(df2['high5'])
# plt.plot(df2['low5'])
# plt.plot(df2['y'])
# plt.show()


x_df = df2[[
  # 'close',
  'high1',
  'low1',
  'high2',
  'low2',
  'high3',
  'low3',
  'high4',
  'low4',
  'high5',
  'low5'
]]
# y_df = df2['y']
y_df = df2['pct_change']



x = x_df.to_numpy()
y = y_df.to_numpy()
y = y.reshape(len(y), 1)

print(x.shape)
print(y.shape)

N, D_in, H, D_out = len(x), len(x[0]), 10, 1

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
    self.w2 = torch.nn.Parameter(torch.randn(D_out, D_in, device=device, dtype=dtype, requires_grad=True))

  def forward(self, x):
    y_pred = x * self.w1 + self.b1
    y_pred = torch.tanh(y_pred)
    y_pred = F.linear(y_pred, self.w2)
    y_pred = torch.tanh(y_pred)

    return y_pred

model = Network1(D_in, D_out)

# ### NEURAL NETWORK MODEL
# model = torch.nn.Sequential(
#   torch.nn.Linear(D_in, H),
#   torch.nn.ReLU(),
#   torch.nn.Linear(H, H),
#   torch.nn.ReLU(),
#   torch.nn.Linear(H, D_out),
#   torch.nn.Tanh()
# )


learning_rate = 1e-2
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# criterion = torch.nn.MSELoss(reduction='sum')


### TRAIN
for t in range(1000):
  y_pred = model(x_train)
  results = y_pred * y_train

  # loss = criterion(y_pred, y_train)
  loss = -(results.sum())
  if t % 100 == 99:
    print(t, loss.item())

  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

results = results.detach().numpy()

plt.plot(results.cumsum())
plt.show()


### TEST
y_pred = model(x_test)
results = y_pred * y_train

# loss = criterion(y_pred, y_test)
loss = -(results.sum())
print("test loss: ", loss.item())

results = results.detach().numpy()

plt.plot(results.cumsum())
plt.show()


end_time = datetime.now() - start_time
print()
print("TIME ELAPSED: ", end_time)