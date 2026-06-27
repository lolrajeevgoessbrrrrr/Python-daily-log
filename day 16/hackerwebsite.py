import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://news.ycombinator.com/"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Inspect told us headlines are in <span class="titleline">
headlines = soup.find_all("span", class_="titleline")

top_10 = []

for i, item in enumerate(headlines[:10]):
    link_tag = item.find("a")        # the <a> tag inside has the text
    title = link_tag.text.strip()
    top_10.append(f"{i+1}. {title}")
    print(f"{i+1}. {title}")

# Save to file
with open("headlines.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(top_10))

print("\n✅ Saved to headlines.txt")