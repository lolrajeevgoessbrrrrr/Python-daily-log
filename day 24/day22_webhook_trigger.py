"""
Python → n8n Webhook Bridge
Sends a JSON payload from Python to an n8n webhook, triggering an automation
workflow. This is the bridge pattern used to connect custom Python logic
(scraping, AI processing, file handling) into n8n's automation pipelines.
"""

import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webhook_trigger.log'),
        logging.StreamHandler()
    ]
)

# NOTE: this is a local n8n test-webhook URL — replace with your own
# n8n instance's webhook URL when reusing this script.
webhook_url = "http://localhost:5678/webhook-test/6468ca2e-0276-4e23-a5d8-a81edf57557e"
payload = {"message": "Hello, from Python", "source": "day22_script"}


def trigger_webhook(url, data):
    """Sends `data` as JSON to the n8n webhook at `url`, logging success or failure."""
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        logging.info(f"Webhook sent successfully. Status: {response.status_code}")
        logging.info(f"Response Body: {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending webhook: {e}")


if __name__ == "__main__":
    trigger_webhook(webhook_url, payload)
