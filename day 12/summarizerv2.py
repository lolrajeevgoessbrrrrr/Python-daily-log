from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarise_file(input_file, output_file):
    try:
        with open(input_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("File not found.")
        return

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Summarise the given text into 3 bullet points and one main takeaway."},
            {"role": "user", "content": content}
        ]
    )

    summary = response.choices[0].message.content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(output_file, "w") as f:
        f.write(f"Summary generated on: {timestamp}\n\n")
        f.write(summary)

    print(f"Done. Summary saved to {output_file}")

input_file = input("Enter input filename: ")
output_file = input("Enter output filename: ")
summarise_file(input_file, output_file)