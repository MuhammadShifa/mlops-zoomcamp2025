import json
import requests 

with open('event.json', 'rt', encoding='utf-8') as f_in:
    event = json.load(f_in)

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(url, json=event)
print(response.json())
