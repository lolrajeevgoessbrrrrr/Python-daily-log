students = [
    {"name": "Rajeev", "marks": 92},
    {"name": "Aman", "marks": 78},
    {"name": "Priya", "marks": 85},
    {"name": "Horikita", "marks": 95},
]

for student in students:
    print(f"{student['name']} scored {student['marks']}")
for student in students: #a loop that prints ONLY students who scored above 80.
    if student['marks'] > 80:
        print(f"{student['name']} has scored above 80 marks.")
    