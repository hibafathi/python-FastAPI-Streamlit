class Student:

    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks

    def calculate_grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 80:
            return "B"
        elif self.marks >= 70:
            return "C"
        elif self.marks >= 60:
            return "D"
        else:
            return "F"

    def display_details(self):
        print("\nRoll Number :", self.roll_no)
        print("Name        :", self.name)
        print("Marks       :", self.marks)
        print("Grade       :", self.calculate_grade())

students = []

n = int(input("Enter number of students: "))

for i in range(n):
    print("\nEnter Student", i + 1, "Details")

    roll_no = int(input("Roll Number: "))
    name = input("Name: ")
    marks = float(input("Marks: "))

    student = Student(roll_no, name, marks)
    students.append(student)

for student in students:
    student.display_details()