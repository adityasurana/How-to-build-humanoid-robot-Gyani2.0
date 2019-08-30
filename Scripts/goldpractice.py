n=5
arr=[2, 1, 3, 1, 2]
count=0
for i in range(0,n):
    for j in range(i, n):
        print("i", i, "j", j)
        print("arr[i]", arr[i], "arr[j]", arr[j])
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j], arr[i]
            count += 1
            print(count)

print(count)
        
