"""
Headline Scraper + Emailer
Scrapes the top 10 headlines from Times of India and emails them to yourself
using Gmail's SMTP server. Combines Day 16 (scraping) with Day 18 (email automation).
"""

import logging
import os
import smtplib
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smtp_headline_mailer.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
    logging.error("Missing EMAIL_ADDRESS or EMAIL_APP_PASSWORD in .env file.")
    exit(1)


def scrape_top_headlines(url="https://timesofindia.indiatimes.com/", limit=10):
    """Scrapes up to `limit` unique headlines from the given news URL."""
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find_all("figcaption")

    top_headlines = []
    seen = set()

    for item in headlines:
        text = item.text.strip()
        if text and text not in seen:
            seen.add(text)
            top_headlines.append(text)
        if len(top_headlines) == limit:
            break

    logging.info(f"Scraped {len(top_headlines)} headlines from {url}")
    return top_headlines


def send_headline_email(headlines):
    """Formats headlines into an email body and sends it via Gmail SMTP."""
    if not headlines:
        logging.error("No headlines to send — aborting email send.")
        return

    body_lines = [f"{i}. {h}" for i, h in enumerate(headlines, 1)]
    body = "\n".join(body_lines)

    msg = MIMEText(body)
    msg["Subject"] = "Today's Top 10 Headlines - TOI"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        logging.info("Headlines emailed successfully.")
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send email: {e}")


if __name__ == "__main__":
    headlines = scrape_top_headlines()
    send_headline_email(headlines)
