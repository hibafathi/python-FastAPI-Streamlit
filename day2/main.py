from util import greet, calculate_grade

name = input("Enter your name: ")
mark = int(input("Enter your mark: "))

print(greet(name))
print("Grade:", calculate_grade(mark))