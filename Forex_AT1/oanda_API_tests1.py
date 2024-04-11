import requests
import json
import dateutil.parser
import matplotlib.pyplot as plt
from main_functions1 import *






data = retrieveOandaPrices('2018-03-01T00:00:00-06:00', '2018-03-02T00:00:00-06:00', 'EUR_USD', 'H1')
formattedData = json.dumps(data, indent=3, sort_keys=True)
print(formattedData)

# priceList = []
# pcList = []
# priceTimeList = []
# for i in range(1, len(data['candles'])):
# 	curPrice = float(data['candles'][i]['mid']['o'])
# 	prePrice = float(data['candles'][i-1]['mid']['o'])
# 	time = data['candles'][i]['time'][:16] + '-06:00'

# 	percentChange = (curPrice - prePrice) / prePrice

# 	priceList.append(curPrice)
# 	pcList.append(percentChange)
# 	priceTimeList.append(dateutil.parser.parse(time))

	# print("curPRICE: ", curPrice, "  prePRICE: ", prePrice, "  TIME: ", time, "  percCHANGE: ", percentChange, )

# print()
# print(len(pcList))


# plt.plot(priceTimeList, pcList)
# plt.xticks(rotation=-90)
# plt.tight_layout()
# plt.show()
