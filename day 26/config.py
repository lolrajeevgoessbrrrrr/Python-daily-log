"""
Day 26 — Config file
Holds non-secret settings that might need to change often,
kept separate from the main script so they're easy to find and edit.
Secrets (API keys) do NOT belong here — those live in .env instead.
"""
 
# Which Groq model to use for AI calls
GROQ_MODEL = "llama-3.3-70b-versatile"
 
# Default keyword to search if the user doesn't provide one
DEFAULT_KEYWORD = "python"
 
# Max number of results to keep when scraping/fetching listings
MAX_RESULTS = 20
 
# Default output filename for saved CSV files
OUTPUT_FILENAME = "results.csv"
 