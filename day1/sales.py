sales=[1200,1500,900,1800,2200,1700,1300]
count=0
total=sum(sales)
mini=min(sales)
maxi=max(sales)
avg=total/len(sales)

for i in range(len(sales)):
    if sales[i]>1500:
        count+=1
print("total sales=",total)
print("minimum sale=",mini)
print("maximum sale=",maxi)
print("average sale =",avg)
print("the number of days which sale greate than 1500=",count)
