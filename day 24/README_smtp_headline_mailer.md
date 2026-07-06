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
2026-07-06 09:00:03 - INFO - Headlines emailed successfully.
```

## Notes
- Logs are written to both console and `smtp_headline_mailer.log`.
- If the site structure changes, the scraper may return 0 headlines — the script logs this and skips sending an empty email rather than failing silently.
