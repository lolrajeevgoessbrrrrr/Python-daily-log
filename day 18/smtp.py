import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# 1. Scrape headlines (from Day 17)
headers = {"User-Agent": "Mozilla/5.0"}
url = "https://timesofindia.indiatimes.com/"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

headlines = soup.find_all("figcaption")

top_10 = []
seen = set()

for item in headlines:
    text = item.text.strip()
    if text and text not in seen:
        seen.add(text)
        top_10.append(text)
    if len(top_10) == 10:
        break

# 2. Build email body from scraped headlines
body_lines = [f"{i}. {h}" for i, h in enumerate(top_10, 1)]
body = "\n".join(body_lines)

msg = MIMEText(body)
msg["Subject"] = "Today's Top 10 Headlines - TOI"
msg["From"] = EMAIL_ADDRESS
msg["To"] = EMAIL_ADDRESS

# 3. Send it
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
    server.send_message(msg)

print("✅ Headlines emailed successfully!")