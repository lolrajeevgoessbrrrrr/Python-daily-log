"""
Day 26 — Environment Variables + Config Files
Demonstrates the pattern: secrets go in .env (never pushed to GitHub),
non-secret settings go in config.py (safe to push, easy to edit).

Setup:
    1. Copy .env.example to .env
    2. Fill in your real GROQ_API_KEY inside .env
    3. Run this script
"""

import os
from dotenv import load_dotenv
import config  # our own config.py file, imported like any module

# Loads variables from the .env file into the environment.
# Without this line, os.getenv() below would return None even if .env exists.
load_dotenv()

# Pull the secret out of the environment — never typed directly in this file.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def check_setup():
    """
    Confirms both the secret (.env) and the config (config.py) loaded correctly.
    This is the kind of sanity check worth running before building anything
    bigger on top of a new setup.
    """
    print("Checking environment setup...\n")

    if GROQ_API_KEY:
        # Never print the real key — just confirm it exists and show a masked version.
        masked = GROQ_API_KEY[:4] + "..." + GROQ_API_KEY[-4:]
        print(f"GROQ_API_KEY loaded: {masked}")
    else:
        print("GROQ_API_KEY is missing! Did you create a .env file from .env.example?")

    print(f"Model from config.py: {config.GROQ_MODEL}")
    print(f"Default keyword from config.py: {config.DEFAULT_KEYWORD}")
    print(f"Max results from config.py: {config.MAX_RESULTS}")
    print(f"Output filename from config.py: {config.OUTPUT_FILENAME}")


if __name__ == "__main__":
    check_setup()