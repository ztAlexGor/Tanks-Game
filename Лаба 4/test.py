a = [1,2,3,4,5]

del a[]

indexes = [2, 3, 5]
for index in sorted(indexes, reverse=True):
    del my_list[index]

print(a)