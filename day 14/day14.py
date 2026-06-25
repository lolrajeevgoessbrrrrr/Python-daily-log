from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are a concise assistant who gives short, direct answers."

def build_fresh_history():
    return [{"role": "system", "content": SYSTEM_PROMPT}]

conversation_history = build_fresh_history()

print("Chat started. Commands: 'quit' to exit, 'clear' to reset memory, 'history' to see message count.\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "quit":
        print("Bye.")
        break

    if user_input.lower() == "clear":
        conversation_history = build_fresh_history()
        print("Memory cleared. Starting fresh.\n")
        continue

    if user_input.lower() == "history":
        messages = len(conversation_history) - 1
        print(f"Messages in memory: {messages}\n")
        continue

    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
        )

        reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        print(f"AI: {reply}\n")

    except Exception as e:
        print(f"Error: {e}\n")