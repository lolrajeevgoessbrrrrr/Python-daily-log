import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://timesofindia.indiatimes.com/"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# TOI uses <figcaption> or <div class="col_l_6"> for headlines
# If one doesn't work, try the other — inspect and adjust
headlines = soup.find_all("figcaption")

top_10 = []
seen = set()  # avoid duplicates

for item in headlines:
    text = item.text.strip()
    if text and text not in seen:
        seen.add(text)
        top_10.append(text)
    if len(top_10) == 10:
        break

for i, h in enumerate(top_10, 1):
    print(f"{i}. {h}")

with open("headlines.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(f"{i+1}. {h}" for i, h in enumerate(top_10)))

print("✅ Done — headlines.txt saved")