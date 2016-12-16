import json
from pprint import pprint


with open('message.json') as data_file:    
    data = json.load(data_file)
pprint(data)

print data["pingPositionBateau"]["x"]
