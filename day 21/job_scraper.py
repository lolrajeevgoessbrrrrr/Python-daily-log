"""
Day 19 - Job Alert Scraper (CLI)
Fetches remote job listings from RemoteOK + Remotive public JSON APIs,
filters by keyword, prints matches to terminal and saves them to CSV.

Usage:
    python job_scraper.py --keyword python
    python job_scraper.py --keyword "data analyst" --output jobs.csv
    python job_scraper.py --keyword react --limit 10
"""

import argparse
import json
import csv
import sys
import requests


REMOTEOK_URL = "https://remoteok.com/api"
REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

# RemoteOK / Remotive block requests that don't look like a real browser.
# A bare "requests" User-Agent gets an instant 403 — this mimics Chrome.
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
    for item in data[1:]:
        title = item.get("position", "")
        company = item.get("company", "")
        tags = [t.lower() for t in item.get("tags", [])]
        location_raw = item.get("location", "Remote")
        location = location_raw.encode("latin-1").decode("utf-8", errors="replace")

        keyword_lower = keyword.lower()
        title_match = keyword_lower in title.lower()
        tag_match = keyword_lower in tags

        if not (title_match or tag_match):
            continue

        jobs.append({
            "source": "RemoteOK",
            "title": title,
            "company": company,
            "location": location,
            "url": item.get("url", ""),
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
        title = item.get("title", "")
        tags = [t.lower() for t in item.get("tags", [])]
        keyword_lower = keyword.lower()
        title_match = keyword_lower in title.lower()
        tag_match = keyword_lower in tags

        if not (title_match or tag_match):
            continue
        jobs.append({
            "source": "Remotive",
            "title": title,
            "company": item.get("company_name", ""),
            "location": item.get("candidate_required_location", "Remote"),
            "url": item.get("url", ""),
        })
    return jobs


def print_jobs(jobs):
    """Print job matches to the terminal in a readable format."""
    if not jobs:
        print("No matching jobs found.")
        return

    print(f"\nFound {len(jobs)} matching job(s):\n")
    for job in jobs:
        print(f"[{job['source']}] {job['title']} — {job['company']}")
        print(f"    Location: {job['location']}")
        print(f"    Apply: {job['url']}\n")


def save_to_csv(jobs, filename):
    """Save job matches to a CSV file using DictWriter."""
    if not jobs:
        print("Nothing to save — no matches found.")
        return

    fieldnames = ["source", "title", "company", "location", "url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Saved {len(jobs)} job(s) to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Search RemoteOK + Remotive for remote jobs matching a keyword."
    )
    parser.add_argument(
        "--keyword", required=True, help="Job keyword to search for (e.g. python, react, data analyst)"
    )
    parser.add_argument(
        "--output", default="jobs.csv", help="CSV filename to save results (default: jobs.csv)"
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Max number of results to keep (default: all)"
    )
    args = parser.parse_args()

    print(f"Searching for '{args.keyword}' jobs...")

    all_jobs = fetch_remoteok(args.keyword) + fetch_remotive(args.keyword)

    if args.limit:
        all_jobs = all_jobs[: args.limit]

    print_jobs(all_jobs)
    save_to_csv(all_jobs, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)