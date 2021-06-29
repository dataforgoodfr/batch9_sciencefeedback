import json
import requests


url = 'http://127.0.0.1:8080/predictions/bert'
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

test = 'coucou'
response = requests.post(url, data=json.dumps(test), headers=headers)
print(response.content)
