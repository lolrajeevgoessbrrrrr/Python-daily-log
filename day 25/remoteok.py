"""
Day 25 — Freelance/Remote Job Listing Scraper (CLI)
Pulls remote job listings from RemoteOK + Remotive public JSON APIs,
filters by keyword, prints matches, and saves them to CSV.

Built on the same working approach as Day 19's job_scraper.py —
two public JSON APIs beat fighting a site's rendered HTML or its
anti-bot layer (Indeed) any day.

Usage:
    python freelance_scraper.py
"""

import json
import csv
import requests

REMOTEOK_URL = "https://remoteok.com/api"
REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

# Bare "requests" User-Agent gets blocked instantly — this mimics a real browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_remoteok(keyword):
    """Fetch and filter jobs from RemoteOK's public JSON API."""
    jobs = []
    try:
        response = requests.get(REMOTEOK_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = json.loads(response.content.decode("utf-8"))
    except requests.exceptions.RequestException as e:
        print(f"[RemoteOK] Could not fetch jobs: {e}")
        return jobs

    # First item in RemoteOK's response is a metadata blob, not a job — skip it
    keyword_lower = keyword.lower()
    for item in data[1:]:
        title = item.get("position", "")
        tags = [t.lower() for t in item.get("tags", [])]

        if keyword_lower in title.lower() or keyword_lower in tags:
            jobs.append({
                "source": "RemoteOK",
                "title": title,
                "company": item.get("company", ""),
                "link": item.get("url", ""),
            })
    return jobs


def fetch_remotive(keyword):
    """Fetch and filter jobs from Remotive's public JSON API."""
    jobs = []
    try:
        response = requests.get(
            REMOTIVE_URL, params={"search": keyword}, headers=HEADERS, timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Remotive] Could not fetch jobs: {e}")
        return jobs

    for item in data.get("jobs", []):
        jobs.append({
            "source": "Remotive",
            "title": item.get("title", ""),
            "company": item.get("company_name", ""),
            "link": item.get("url", ""),
        })
    return jobs


def save_to_csv(jobs, filename="freelance_listings.csv"):
    """Write matched jobs to a CSV file."""
    if not jobs:
        print("No jobs to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "company", "link"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Saved {len(jobs)} listings to {filename}")


def main():
    keyword = input("Enter a job keyword to search (e.g. python, automation, n8n): ").strip()

    print(f"Fetching listings for '{keyword}'...")
    all_jobs = fetch_remoteok(keyword) + fetch_remotive(keyword)

    print(f"Found {len(all_jobs)} matching listings.")
    for job in all_jobs:
        print(f"  [{job['source']}] {job['title']} — {job['company']}")

    save_to_csv(all_jobs)


if __name__ == "__main__":
    main()