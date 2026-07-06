"""
Text Summarizer using Groq AI
Reads a text file, sends it to Groq's LLM, and saves a concise summary
(3 bullet points + 1 main takeaway) to an output file.
"""

import logging
import os
from groq import Groq
from dotenv import load_dotenv

# Logging setup — writes to both console and a log file, so failures
# are traceable later even if the terminal window is long closed.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('summarizer.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Fail fast and clearly if the API key is missing, instead of letting
# the Groq client throw a confusing auth error later.
if not api_key:
    logging.error("GROQ_API_KEY not found in environment. Check your .env file.")
    exit(1)

client = Groq(api_key=api_key)


def summarise_file(input_filename, output_filename):
    """Reads input_filename, summarises its contents via Groq, writes result to output_filename."""

    # Reading the file is a separate risk from the API call — isolate it
    # so we know exactly which step failed.
    try:
        with open(input_filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_filename}")
        return
    except Exception as e:
        logging.error(f"Unexpected error reading {input_filename}: {e}")
        return

    # The API call is the most likely failure point (network issues,
    # rate limits, invalid key) — handled separately from file I/O.
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarises text clearly and concisely into 3 bullet points and one main takeaway."},
                {"role": "user", "content": f"Summarise this text:\n\n{content}"}
            ]
        )
        summary = response.choices[0].message.content
        logging.info("Summary generated successfully via Groq API.")
    except Exception as e:
        logging.error(f"Groq API error: {e}")
        return

    # Writing output is its own risk too (disk full, permissions, etc.)
    try:
        with open(output_filename, "w") as file:
            file.write(summary)
        logging.info(f"Summary saved to {output_filename}")
    except Exception as e:
        logging.error(f"Failed to write summary to {output_filename}: {e}")


if __name__ == "__main__":
    input_file = input("Enter the filename to summarise: ")
    output_file = "summary_" + input_file
    summarise_file(input_file, output_file)
