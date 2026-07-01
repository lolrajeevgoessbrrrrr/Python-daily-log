import requests
import argparse
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

parser = argparse.ArgumentParser()
parser.add_argument("--email", help="Email address to send headlines to.")
parser.add_argument("--url", default="https://timesofindia.indiatimes.com/", help="URL to scrape headlines from")
parser.add_argument("--count", type=int, default=10, help="Number of headlines to fetch")
args = parser.parse_args()
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# 1. Scrape headlines (from Day 17)
headers = {"User-Agent": "Mozilla/5.0"}
url = args.url
count = args.count

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

headlines = soup.find_all("figcaption")

result = []
seen = set()

for item in headlines:
    text = item.text.strip()
    if text and text not in seen:
        seen.add(text)
        result.append(text)
    if len(result) == count:
        break

# 2. Build email body from scraped headlines
body_lines = [f"{i}. {h}" for i, h in enumerate(result, 1)]
body = "\n".join(body_lines)

msg = MIMEText(body)
msg["Subject"] = f"Today's Top {count} Headlines - TOI"
msg["From"] = EMAIL_ADDRESS
msg["To"] = args.email if args.email else EMAIL_ADDRESS

# 3. Send it
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
    server.send_message(msg)

print("✅ Headlines emailed successfully!")