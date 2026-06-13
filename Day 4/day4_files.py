def save_note(note):
    with open("my_log.txt", "a") as file:
        file.write(note + "\n")

def show_all_notes():
    try:
        with open("my_log.txt", "r") as file:
            content = file.read()
        print("\n--- Your Notes ---")
        print(content)
    except FileNotFoundError:
        print("No notes yet.")

while True:
    print("\n1. Add note")
    print("2. View all notes")
    print("3. Quit")
    
    choice = input("Choose: ")
    
    if choice == "1":
        note = input("Type your note: ")
        save_note(note)
        print("Saved.")
    elif choice == "2":
        show_all_notes()
    elif choice == "3":
        print("Bye.")
        break
    else:
        print("Invalid choice.")