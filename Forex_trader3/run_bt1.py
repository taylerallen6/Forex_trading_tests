import sqlalchemy as db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Bt1 import bt1 as bt


if __name__ == "__main__":
  # sqlite_file = 'forex2.db'
  sqlite_file = '10_min_forex.db'
  engine = db.create_engine('sqlite:///'+ sqlite_file)
  conn = engine.connect()

  currency_pair = 'eur_usd1'
  # currency_pair = 'usd_cad1'
  # currency_pair = 'usd_jpy1'
  # currency_pair = 'gbp_usd1'

  # query_val = 200000
  query_val = 100000000
  sql = "SELECT * FROM {} WHERE rowid <= {}".format(currency_pair, query_val)
  # query_val = 600000
  # sql = "SELECT * FROM {} WHERE rowid >= {}".format(currency_pair, query_val)
  df = pd.read_sql(sql, conn)
  print(df.head())

  print()
  print("data imported")
  print()

  # df = add_data.format_data(df)
  print()
  print("data formated")
  print()

  stats = bt.run_bt(df)
  # print(stats[0])
  diff = np.diff(stats[0])
  wins = diff[diff > 0]
  losses = diff[diff < 0]

  print("average win: ", wins.mean())
  print("average loss: ", losses.mean())
  print("max win: ", diff.max())
  print("max loss: ", diff.min())

  plt.plot(stats[0])
  plt.show()