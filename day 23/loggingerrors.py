import requests   # lets Python make web requests (call APIs, webhooks)
import logging    # the logging module itself

logging.basicConfig(              # one-time setup, before any logging happens
    level=logging.INFO,           # only show INFO and above (ignore DEBUG)
    format='%(asctime)s - %(levelname)s - %(message)s',   # what each log line looks like
    handlers=[                    # WHERE to send logs — a list of destinations
        logging.FileHandler('app.log'),   # destination 1: write to app.log
        logging.StreamHandler()           # destination 2: also print to console
    ]
)

webhook_url = "http://localhost:5678/webhook-test/..."   # your n8n webhook address
payload = {"message": "Hello, from Python", "source": "day22_script"}  # data you're sending

try:
    response = requests.post(webhook_url, json=payload)   # actually send the request
    response.raise_for_status()   # if status code is 4xx/5xx, force an exception NOW
    logging.info(f"Webhook sent successfully. Status: {response.status_code}")  # log success
    logging.info(f"Response Body: {response.text}")   # log what n8n sent back
except requests.exceptions.RequestException as e:   # catches ANY request-related failure
    logging.error(f"Error sending webhook: {e}")   # log the failure instead of crashing