import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import time

from thinker1 import Brain1

# create connection
conn = sqlite3.connect('../../Python_projects/Forex_AT2/Forex_AT2.db')
c = conn.cursor()


spreadVal = .0002
profitVal = .0003
moveVal = spreadVal + profitVal

c.execute('''SELECT * FROM OandaDataTableD1_5years''',)
retRows = c.fetchall()
df_eurusd = pd.DataFrame(retRows, columns=['Datetime', 'Frequency', 'Close', 'High', 'Low', 'Open', 'Volume'])
df_eurusd.set_index('Datetime', inplace=True)
df_eurusd.dropna(inplace=True)
# print(df_eurusd.head())

df_pc = pd.DataFrame()
for i in range(1, 11):
	df_pc['pastPricePc_'+str(i)] = (df_eurusd['Close'].shift(i)-df_eurusd['Open'].shift(i)) / df_eurusd['Open'].shift(i)
	df_pc['pastVolumePc_'+str(i)] = (df_eurusd['Volume'].shift(i)-df_eurusd['Volume'].shift(i+1)) / df_eurusd['Volume'].shift(i+1)
	df_pc['pastVolatilityPc_'+str(i)] = ((df_eurusd['High'].shift(i)-df_eurusd['Low'].shift(i))-(df_eurusd['High'].shift(i+1)-df_eurusd['Low'].shift(i+1))) / (df_eurusd['High'].shift(i+1)-df_eurusd['Low'].shift(i+1))

df_pc.dropna(inplace=True)
# print(df_pc.head())




start_time = time.time()


# testAr = np.array([[1,2,3], [4,5,6], [7,8,9]])
testAr = np.array(df_pc)
testAr = testAr[-100:]


Brain1_1 = Brain1(len(testAr[0]))
np.apply_along_axis(Brain1_1.step, 1, testAr)
print()
# print(Brain1_1.memories)
print("number of memories: ",len(Brain1_1.memories))
print()

# aprioriAr = Brain1_1.apriori()
# print(aprioriAr)
# print(max(aprioriAr))

Brain1_1.NNtrain(1)

print()
elapsed_time = time.time() - start_time
print(elapsed_time)