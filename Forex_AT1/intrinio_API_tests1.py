import requests
import json
from main_functions1 import *




data = retrieveIntrinioData('$GDP', 'level', '2017-03-10', '2018-03-10', 'quarterly')
formattedData = json.dumps(data, indent=3, sort_keys=True)
print(formattedData)

newData = data['data']

for data in newData:
	print(data['value'])

print()
print(newData)