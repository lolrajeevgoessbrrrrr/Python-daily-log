from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(system_prompt, user_message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

# Test 3 different system prompts on the same question
question = "What is discipline?"

print(ask("You are a stoic philosopher.", question))
print("---")
print(ask("You are a sports coach talking to a lazy athlete.", question))
print("---")
print(ask("You are a monk who has practiced for 40 years.", question))