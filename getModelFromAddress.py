import urllib
import requests
import json

#Definition of parameters
text = input("Please enter an address: ")
base_url="https://api3.geo.admin.ch/rest/services/api/SearchServer?"
parameters = {"searchText": text, "origins": "address", "type": "locations",}

#Request
r = requests.get(f"{base_url}{urllib.parse.urlencode(parameters)}")

data = json.loads(r.content)
print(data)