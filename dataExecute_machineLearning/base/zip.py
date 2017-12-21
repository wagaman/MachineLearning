__author__ = 'sss'

a = [1,2,3]
b = [4,5,6]
c = [4,5,6,7,8]
zipped = zip(a, b)
zipped_2 = zipped

print(list(zip(*zipped)))

print(list(zipped_2))
print(list(zip(a, b)))


#行列互换
a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(list(zip(*a)))