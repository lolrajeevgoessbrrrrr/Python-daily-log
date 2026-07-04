import requests
import json

webhook_url = "http://localhost:5678/webhook-test/6468ca2e-0276-4e23-a5d8-a81edf57557e"
payload = { "message": "Hello, from Python", "source": "day22_script" }

response = requests.post(webhook_url, json=payload)

print("Status Code:", response.status_code)
print("Response Body:", response.text)