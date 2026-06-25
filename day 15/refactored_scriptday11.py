"""
Module: refactored_scriptday11.py
Purpose: This script reads a text file, sends its content to the Groq API for summarization, and saves the summary to a new file.
The summary consists of 3 bullet points and one main takeaway.
Author: Rajeev
"""
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def summarise_file(input_filename, output_filename):
    """Summarises the content of a text file using the Groq API and saves the summary to a new file."""
    try:
        with open(input_filename, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: {input_filename} not found.")
        return
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarises text clearly and concisely into 3 bullet points and one main takeaway."},
                {"role": "user", "content": f"Summarise this text:\n\n{content}"}
            ]
        )
        summary = response.choices[0].message.content
    except Exception as e:
        print(f"API error: {e}")
        return
    
    with open(output_filename, "w") as file:
        file.write(summary)
    
    print(f"Done! Summary saved to {output_filename}")

input_file = input("Enter the filename to summarise: ")
output_file = "summary_" + input_file
summarise_file(input_file, output_file)