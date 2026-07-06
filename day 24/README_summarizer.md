# AI Text Summarizer

Reads a text file and generates a concise summary (3 bullet points + 1 main takeaway) using Groq's LLM.

## Tech Stack
- Python
- Groq API (`llama-3.3-70b-versatile`)
- `python-dotenv` for API key management
- `logging` module for error tracking

## How to Run
1. Create a `.env` file with:
   ```
   GROQ_API_KEY=your_key_here
   ```
2. Install dependencies:
   ```
   pip install groq python-dotenv
   ```
3. Run the script:
   ```
   python summarizer.py
   ```
4. Enter the filename you want summarised when prompted.

## Example
```
Enter the filename to summarise: headlines.txt
Done! Summary saved to summary_headlines.txt
```

## Notes
- Logs are written to both the console and `summarizer.log` for debugging.
- Handles missing files, API failures, and write errors gracefully instead of crashing.
