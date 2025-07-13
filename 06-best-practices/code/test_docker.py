import os
import json

import requests

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

with open("event.json", "rt", encoding="utf-8") as f_in:
    event = json.load(f_in)

url = "http://localhost:8080/2015-03-31/functions/function/invocations"
response = requests.post(url, json=event, timeout=int(REQUEST_TIMEOUT))
print(response.json())
