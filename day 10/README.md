# Day 10 — JSON Deep Dive

## What I learned
- JSON is just nested Python dicts and lists combined
- Looping through lists of dictionaries (list of student records)
- The `json` module: `json.dumps()` / `json.loads()` for string ↔ dict conversion
- `json.dump()` / `json.load()` for writing/reading JSON directly to/from files
- `enumerate()` for numbering items while looping

## Files
- `stringdict.py` — nested dict practice (city weather data)
- `studenting.py` — looping through a list of student dicts, filtering by marks
- `weatherdatajson.py` — json.dumps/loads practice
- `topicsaving.py` — main project: a CLI tool that saves study topics to a JSON file and reloads them on the next run, proving persistence

## How to run