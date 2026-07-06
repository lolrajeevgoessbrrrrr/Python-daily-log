# Python → n8n Webhook Bridge

Sends a JSON payload from a Python script to an n8n webhook, triggering an n8n automation workflow. This is the core pattern for connecting custom Python logic (scraping, AI processing, file handling) into n8n pipelines.

## Tech Stack
- Python
- `requests` library
- n8n (self-hosted, localhost:5678)
- `logging` module for error tracking

## How to Run
1. Have an n8n workflow running locally with a Webhook trigger node active.
2. Copy your webhook's test URL into the `webhook_url` variable.
3. Install dependencies:
   ```
   pip install requests
   ```
4. Run the script:
   ```
   python day22_webhook_trigger.py
   ```

## Example
```
2026-07-06 09:15:02 - INFO - Webhook sent successfully. Status: 200
2026-07-06 09:15:02 - INFO - Response Body: {"message":"Workflow was started"}
```

## Notes
- Logs both success and failure cases to console and `webhook_trigger.log`.
- If the webhook URL is invalid or n8n isn't running, the error is logged instead of crashing the script.
