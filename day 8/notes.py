from datetime import date
today = date.today()

while True:
    choice = input("1. Press 1 to add a note\n2. Press 2 to view notes\n3. Press 3 to exit\n")
    if choice == "1":
        note = input("Enter your note: ")
        with open("notes.txt", "a") as file:
            file.write(f"{today}: {note}\n")
            print(f"{today}: Note added successfully!\n")
    elif choice == "2":
        try:
            with open("notes.txt", "r") as file:
                content = file.read()
                print(f"{today}: {content}")
        except FileNotFoundError:
            print(f"{today}: Error: notes.txt file not found. Please create the file and try again.\n")
    elif choice == "3":
        break
    else:
        print(f"{today}: Invalid input. Please try again.\n")