from groq import Groq
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

SYSTEM_PROMPT = "You are a patient tutor who explains things simply, breaks down complex topics into easy steps, and encourages the student when they're stuck."

# This list IS the memory. Every message ever sent/received lives here.
conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def save_conversation():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_{timestamp}.txt"
    
    with open(filename, "w") as file:
        for message in conversation_history:
            if message["role"] != "system":
                role = "You" if message["role"] == "user" else "Tutor"
                file.write(f"{role}: {message['content']}\n\n")
    
    print(f"Conversation saved to {filename}")

print("StudyMate AI — your patient tutor.")
print("Type 'save' to save the conversation, 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye! Keep learning.")
        break
    
    if user_input.lower() == "save":
        save_conversation()
        continue
    
    conversation_history.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
        )
        
        ai_reply = response.choices[0].message.content
        print(f"Tutor: {ai_reply}\n")
        
        conversation_history.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        print(f"Something went wrong: {e}")
        print("Try again or check your internet connection.\n")
