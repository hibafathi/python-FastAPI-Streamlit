total=0
for i in range(5):
    mark=float(input(f"enter the mark for subject {i+1}:"))
    total+=mark
avg=total/5
if avg>=90:
    grade='A'
elif avg>=80:
    grade='B'
elif avg>=70:
    grade='C'
elif avg>=60:
    grade='D'
else:
    grade='F'

print("average mark =",mark)
print("grade is ",grade)
