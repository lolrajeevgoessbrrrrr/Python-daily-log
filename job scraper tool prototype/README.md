# Job Alert Scraper CLI

Searches RemoteOK + Remotive for remote jobs matching a keyword.
Prints results to terminal and saves to CSV.

## Install
pip install requests

## Usage
python job_scraper.py --keyword python
python job_scraper.py --keyword "data analyst" --output data_jobs.csv
python job_scraper.py --keyword react --limit 10

## Output
Terminal print + CSV file with: source, title, company, location, url
