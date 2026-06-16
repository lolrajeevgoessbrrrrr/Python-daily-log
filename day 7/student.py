students = []
def add_student(name, age, city):
    student = {"name": name, "age": age, "city": city}
    students.append(student)
for i in range(3):
    name = input("Enter student name: ")
    age = (input("Enter student age: "))
    try:
        age = int(age)
    except ValueError:
        print("Invalid age. Please enter a number.")
        continue
    city = input("Enter student city: ")
    add_student(name, age, city)
for student in students:
    print(f"Name: {student['name']} ({student['age']}) from {student['city']}")
students[0]["age"] = 20
for student in students:
    print(f"Name: {student['name']} ({student['age']}) from {student['city']}")