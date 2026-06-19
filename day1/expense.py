exp=[]
for i in range(7):
    exps=float(input(f"enter the expense of day{i+1}:"))
    exp.append(exps)
    total=sum(exp)
    mini=min(exp)
    maxi=max(exp)
    avg=sum(exp)/7
print("total expense=",total)
print("lowest expense=",mini)
print("highest expense=",maxi)
print("average expense=",avg)
