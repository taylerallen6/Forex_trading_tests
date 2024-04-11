import pandas as pd


df = pd.read_csv('30_min_major_pairs.csv')
df = df.dropna()
print(df)