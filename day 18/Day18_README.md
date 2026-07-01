# Day 18 — Email Automation with smtplib

## What it does
Scrapes the top 10 headlines from Times of India (building on the Day 16/17 scraper) and emails them straight to your inbox using Python's built-in `smtplib`.

## Tech stack
- `requests` — fetch the page
- `BeautifulSoup` — parse headlines
- `smtplib` + `email.mime.text` — send the email
- `python-dotenv` — keep credentials out of the code

## How it works
1. Scrapes TOI homepage for `figcaption` tags, dedupes, keeps top 10
2. Builds a numbered email body from the headlines
3. Sends via Gmail SMTP (`smtp.gmail.com:587`) using an app password loaded from `.env`

## Setup
```bash
pip install requests beautifulsoup4 python-dotenv
```

Create a `.env` file in the same folder:
```
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_APP_PASSWORD=your16digitapppassword
```

> Note: use a Gmail **App Password**, not your regular password. Enable 2FA on your Google account, then generate one under Google Account → Security → App Passwords.

## How to run
```bash
python day18_scraper_email.py
```

That's it — no arguments, sends to your own inbox by default.

## What I learned
- Sending email programmatically via SMTP + MIME
- Why `.env` files must be actual files, not directories (silent `load_dotenv()` failure if the path resolves wrong)
- Deduplicating scraped text with a `set()` before appending to a results list

## Known limitation
URL, recipient email, and headline count are all hardcoded. Fixed in Day 19 with `argparse`.
