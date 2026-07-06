# Headline Scraper + Emailer

Scrapes the top 10 headlines from Times of India and emails them to yourself automatically using Gmail SMTP.

## Tech Stack
- Python
- `requests` + `BeautifulSoup` for scraping
- `smtplib` for sending email via Gmail
- `python-dotenv` for credentials
- `logging` module for error tracking

## How to Run
1. Create a `.env` file with:
   ```
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_APP_PASSWORD=your_gmail_app_password
   ```
   (Use a Gmail **App Password**, not your regular password — generate one in your Google Account security settings.)
2. Install dependencies:
   ```
   pip install requests beautifulsoup4 python-dotenv
   ```
3. Run the script:
   ```
   python smtp_headline_mailer.py
   ```

## Example
```
2026-07-06 09:00:01 - INFO - Scraped 10 headlines from https://timesofindia.indiatimes.com/

# AI Text Summarizer

Reads a text file and generates a concise summary (3 bullet points + 1 main takeaway) using Groq's LLM.

## Tech Stack
- Python
- Groq API (`llama-3.3-70b-versatile`)
- `python-dotenv` for API key management
- `logging` module for error tracking

## How to Run
1. Create a `.env` file with:
   ```
   GROQ_API_KEY=your_key_here
   ```
2. Install dependencies:
   ```
   pip install groq python-dotenv
   ```
3. Run the script:
   ```
   python summarizer.py
   ```
4. Enter the filename you want summarised when prompted.

## Example
```
Enter the filename to summarise: headlines.txt
Done! Summary saved to summary_headlines.txt
```

## Notes
- Logs are written to both the console and `summarizer.log` for debugging.
- Handles missing files, API failures, and write errors gracefully instead of crashing.

2026-07-06 09:00:03 - INFO - Headlines emailed successfully.
```

## Notes
- Logs are written to both console and `smtp_headline_mailer.log`.
- If the site structure changes, the scraper may return 0 headlines — the script logs this and skips sending an empty email rather than failing silently.

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
