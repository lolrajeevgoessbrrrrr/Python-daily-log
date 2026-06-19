import json
import os

FILENAME = "topics.json"

def load_topics():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

def save_topics(topics):
    with open(FILENAME, "w") as file:
        json.dump(topics, file, indent=4)

topics = load_topics()

while True:
    choice = input("\n1. Add topic\n2. View topics\n3. Quit\n")
    
    if choice == "1":
        topic = input("Enter topic learned: ").strip()
        if topic:
            topics.append(topic)
            save_topics(topics)
            print(f"Saved: {topic}")
        else:
            print("Topic cannot be empty.")
    elif choice == "2":
        for i, t in enumerate(topics, 1):
            print(f"{i}. {t}")
    elif choice == "3":
        break
    else:
        print("Invalid input.")