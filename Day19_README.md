# Day 19 — argparse + CLI Packaging

## What it does
Takes the Day 18 email scraper and makes it configurable from the command line instead of hardcoded — target URL, headline count, and recipient email can all be set at runtime.

## Tech stack
- `argparse` — CLI argument parsing
- `requests`, `BeautifulSoup` — scraping
- `smtplib`, `email.mime.text` — sending
- `python-dotenv` — credentials

## Why this matters
Day 18's script only worked for one site, one headline count, one recipient. If a client wants a different source or a different inbox, you'd have to open the code and edit it by hand. That's not something you ship to a client. `argparse` turns the script into a real command-line tool — configurable without touching a single line of code.

## Arguments

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--email` | str | your own address | Email address to send headlines to |
| `--url` | str | TOI homepage | URL to scrape headlines from |
| `--count` | int | 10 | Number of headlines to fetch |

## Setup
```bash
pip install requests beautifulsoup4 python-dotenv
```

`.env` file (same as Day 18):
```
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_APP_PASSWORD=your16digitapppassword
```

## How to run
Default (no arguments — uses TOI, 10 headlines, sends to yourself):
```bash
python day19_scraper_cli.py
```

Custom count:
```bash
python day19_scraper_cli.py --count 5
```

Full custom run:
```bash
python day19_scraper_cli.py --url "https://timesofindia.indiatimes.com/" --count 3 --email client@gmail.com
```

## What I learned
- `argparse.ArgumentParser()` and `add_argument()` — building a CLI "form" for inputs
- `type=int` for numeric arguments (CLI args are strings by default)
- Sensible defaults so the script still runs safely with zero arguments
- Why naming a file the same as an imported library (`argparse.py`) causes shadowing bugs

## Next step
Day 20 moves this logic into a Streamlit web UI — no terminal required, just a browser form.
