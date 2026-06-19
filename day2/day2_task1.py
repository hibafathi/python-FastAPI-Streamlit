import json

students = [
    {"name": "Ali", "age": 20, "mark": 85},
    {"name": "Sara", "age": 21, "mark": 90},
    {"name": "John", "age": 19, "mark": 78},
    {"name": "Maya", "age": 22, "mark": 95},
    {"name": "Tom", "age": 20, "mark": 88}
]

# Save to JSON
with open("students.json", "w") as file:
    json.dump(students, file, indent=2)

print("Students saved successfully!\n")

# Read from JSON
with open("students.json", "r") as file:
    data = json.load(file)

print("Student Details:")
for student in data:
    print(
        f"Name: {student['name']}, "
        f"Age: {student['age']}, "
        f"Mark: {student['mark']}"
    )